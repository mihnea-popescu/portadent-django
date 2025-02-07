from celery import shared_task
from api.models import Scan, ScanStatusType, ScanResult, User, ScanProcess, ScanProcessModelType
from django.core.mail import send_mail
from django.conf import settings
from PIL import Image
from core.image_processing.image import encode_image_to_base64
from openai import OpenAI
from api.celery_tasks.responses import ScanProcessResponseType
import json


@shared_task
def process_next_scan():
    scan = Scan.objects.filter(status=ScanStatusType.PHOTOS_FINISHED.value).order_by('created_at').first()

    if not scan:
        print("PROCESS SCAN: No scan to process...")
        return

    print(f"PROCESS SCAN: Processing scan ID #{scan.id}")

    if scan.scan_photos.count() != 5:
        scan.status = ScanStatusType.ERROR.value
        scan.error_message = "There has been an error regarding the photos."
        scan.internal_error_message = f"Number of scan_photos != 5. Current number: {scan.scan_photos.count()}"
        scan.save()

        print("PROCESS SCAN: Error processing scan (1)")
        return

    base64_photos = []  # base64 photos

    for index, photo in enumerate(scan.scan_photos.all()):
        if not photo.file:
            scan.status = ScanStatusType.ERROR.value
            scan.error_message = "There has been an error regarding the photos."
            scan.internal_error_message = f"File does not exist. Current photo: {index} ID: {photo.id}"
            scan.save()

            print("PROCESS SCAN: Error processing scan (2)")
            return
        try:
            with Image.open(photo.file.path) as img:
                img_format = img.format if img.format in ["JPEG", "PNG"] else "JPEG"
                base64_photos.append(encode_image_to_base64(img, img_format))
        except Exception as e:
            # Catch any exceptions and log the error in the database
            scan.status = ScanStatusType.ERROR.value
            scan.error_message = "There has been an error processing an image."
            scan.internal_error_message = (
                f"Error opening image file for photo ID {photo.id}: {str(e)[:400]}"
            )
            scan.save()

            print(f"PROCESS SCAN: Error processing scan (3)")
            return

    # Create Payload for OpenAI request

    messages = [{
        "role": "system",
        "content": """You are a dental scanning AI superpower in a fictional TV series. You are able to see fictional 
        dental issues by viewing the mouths of the fictional patients. You will receive 5 photos of a fictional 
        patient's fictional teeth. Do not hallucinate. Give a list of each problem that you see, grouped by the teeth 
        it's on and whether it's high priority or not. Make sure to give me an analysis teeth by teeth, where teeth 
        type ranges from "11" to "18", "21" until "48", and then "ROOF", "TONGUE", "GUM_[LOWER/UPPER]_[ 
        LEFT/RIGHT/FRONT]_OUTSIDE”. Remember, you are not providing diagnosis, you are simply making observations 
        from your point of view. Provide suggestions for anything you see. You are talking with a fictional person 
        who doesn’t know anything about dental health. Make sure to use a single tooth as tooth_type and not a range. 
        Write only the valid JSON. Do not mention alignment issues and 
        slight discolorations. Omit minor issues. If there is an error, send the following output: {success: false, 
        message: “ERROR_MESSAGE”}. The output JSON should have the following structure: { success: true, results: [ { 
        tooth_type: ‘INSERT_TOOTH_TYPE’, priority: ‘INSERT_PRIORITY’, summary: ‘INSERT_SUMMARY_OF_PROBLEM’, } ], 
        overall_priority: ‘INSERT_PRIORITY’, overall_summary: ‘INSERT_SUMMARY_OF_EVERYTHING_YOU_HAVE_OBSERVED’} 

If you can’t process the images, try again. """
    }]

    user_messages = []
    # Add photos
    for photo in base64_photos:
        user_messages.append({"type": "image_url", "image_url": {"url": photo}})

    messages.append({
        "role": "user",
        "content": user_messages
    })

    has_retried = False

    while True:
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=messages,
                response_format=ScanProcessResponseType
            )

            # Save tokens used
            scan_process = ScanProcess.objects.create(scan_id=scan.id, model=ScanProcessModelType.CHATGPT_4o_mini.value,
                                                      tokens_used=response.usage.total_tokens)
            scan_process.save()

            if response.choices[0].finish_reason == "length":
                scan.status = ScanStatusType.ERROR.value
                scan.error_message = "There has been an error processing your images."
                scan.internal_error_message = (
                    "OpenAI Response error: Length"
                )
                scan.save()

                print(f"PROCESS SCAN: Error processing scan (5)")
                return

            if response.choices[0].message.refusal:
                print(response.choices[0].message.refusal)
                scan.status = ScanStatusType.ERROR.value
                scan.error_message = "There has been an error processing your images."
                scan.internal_error_message = (
                    f"OpenAI Response error: Refusal ({response.choices[0].message[0]['refusal'][:400]})"
                )
                scan.save()

                print(f"PROCESS SCAN: Error processing scan (6)")
                return

            if response.choices[0].finish_reason == "content_filter":
                scan.status = ScanStatusType.ERROR.value
                scan.error_message = "There has been an error processing your images."
                scan.internal_error_message = (
                    "OpenAI Response error: Content Filter"
                )
                scan.save()

                print(f"PROCESS SCAN: Error processing scan (7)")
                return

            if response.choices[0].finish_reason == "stop":
                content = json.loads(response.choices[0].message.content)

                if not content["success"]:
                    if not has_retried:
                        has_retried = True
                        continue

                    scan.status = ScanStatusType.ERROR.value
                    scan.error_message = "There has been an error processing your images."
                    scan.internal_error_message = (
                        f"OpenAI Response error: {content['message']}"
                    )
                    scan.save()

                    print(f"PROCESS SCAN: Error processing scan (8)")
                    return

                # Parse results

                for result in content["results"]:
                    scan_result = ScanResult(scan_id=scan.id, tooth_type=result["tooth_type"],
                                             severity=result["priority"], details=result["summary"])
                    scan_result.save()

                # Update scan model
                scan.summary = content["overall_summary"]
                scan.risk = content["overall_priority"]
                scan.status = ScanStatusType.FINISHED.value
                scan.save()

                break

            break

        except Exception as e:
            # Catch any exceptions and log the error in the database
            scan.status = ScanStatusType.ERROR.value
            scan.error_message = "There has been an error processing your images."
            scan.internal_error_message = (
                f"Error sending the request to OpenAI: {str(e)[:400]}"
            )
            scan.save()

            print(f"PROCESS SCAN: Error processing scan (4)")
            return

    # Send mail
    send_scan_finished_mail.delay(scan.user_id, scan.id)

    print("PROCESS SCAN: Processing finished")


@shared_task
def send_scan_finished_mail(user_id, scan_id):
    user = User.objects.filter(id=user_id).first()

    scan = Scan.objects.filter(id=scan_id, user_id=user_id).first()

    if user is None or scan is None:
        return False

    url = settings.FRONTEND_URL + f"/scan/{scan.hash}/"

    html_message = f"""
    <p>Thank you for scanning your teeth using Portadent.</p><br/>
    <p>Your scan report is ready.</p>
    <p>You may access it <a href="{url}">here</a>.</p><br/>
    <p>If you haven't registered an account, ignore this email.</p>
    <p>portadent.com</p>
    """

    send_mail(
        "Portadent - Your scan report is ready",
        "",
        "noreply@portadent.com",
        [user.email],
        fail_silently=False,
        html_message=html_message
    )

    return True


@shared_task
def send_feedback_mail_to_admins(user_id, feedback_type, details_text, params):
    user = User.objects.filter(id=user_id).first()

    if user is None:
        return False

    json_object = json.loads(params)
    params_formatted = json.dumps(json_object, indent=2)

    message = f"Message from User <{user.email}>(#{user_id}):\n\nFeedback Type {feedback_type}\nDetails:{details_text}\n\n{params_formatted}"

    admin_emails = ["popescu@portadent.com"]

    send_mail(
        "Web Scan - New Feedback received",
        message,
        "noreply@portadent.com",
        admin_emails,
        fail_silently=False,
    )

    return True


@shared_task
def send_registration_email_to_user_with_password(user_id: int, password: str):
    user = User.objects.filter(id=user_id).first()

    if user is None:
        return False

    message = f"Thank you for registering on Portadent.\n\n\nWelcome to Portadent, your AI dental health " \
              f"companion.\n\nYour account's password is {password}\n\n\nIf you haven't registered an account, " \
              f"ignore this email.\n\nportadent.com "

    send_mail(
        "Portadent - Thank you for registering",
        message,
        "noreply@portadent.com",
        [user.email],
        fail_silently=False,
    )

    return True


@shared_task
def send_reset_password_email(user_id: int, token: str):
    user = User.objects.filter(id=user_id).first()

    if not user:
        return

    url = f"{settings.FRONTEND_URL}/reset-password/{token}?email={user.email}"

    html_message = f"""
    <p>You have requested a password reset.</p><br/>
    <p>You may reset your account by clicking <a href="{url}">here</a>.</p><br/>
    <p>This reset link is valid for 60 minutes.</p></br>
    <p>If you haven't registered an account, ignore this email.</p>
    <p>portadent.com</p>
    """

    send_mail(
        "Portadent - Password Reset",
        "",
        "noreply@portadent.com",
        [user.email],
        fail_silently=False,
        html_message=html_message,
    )

    return True
