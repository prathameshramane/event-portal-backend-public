from io import BytesIO
from xhtml2pdf import pisa
from django.conf import settings
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from django.core.mail import EmailMessage

# Models
from .models import Entry, Event

MAIL_SUBJECT = "Registration Successful"
MAIL_BODY = '''Hey participant,

You have successfully registered for VCET AVAHAN 2023! Kindly find the attached invoice for the registered event.

Following are some of the common rules:-
●	Captain of the team should report before half an hour for the match. 
●	No players should be repeated from the same department.
●	Referee’s/Umpire’s decision will be final. 
●	Team will be disqualified if any team member is involved in any violence. 
●	Identity cards of each player are mandatory during the match for verification. 
●	In case of improper ID cards, players must present the current year fee receipt along with a photo id proof (eg. Aadhar card, driving license etc.) 
●	Undertaking letter and shoes is compulsory.
●	Only team leader will contact the event coordinator during their matches.

We hope you are geared up for the event! Good luck!

Regards,
VCET Sports Committee.'''


def send_mail(email, subject, body, pdf):
    try:
        subject = subject
        body = body
        recipient_list = [email]
        msg = EmailMessage(subject=subject, body=body,
                           from_email=settings.EMAIL_HOST_USER, to=recipient_list)
        msg.attach('invoice.pdf', pdf, 'application/pdf')
        msg.send()
    except Exception as e:
        print(e)


def send_register_success(email, entry):
    try:
        data = {
            'unique_code': entry.code,
            'event_name': entry.event.name,
            'amount_paid': entry.event.amount,
            'event_head': entry.event.event_head.name,
            'head_contact_1': entry.event.contact_1,
            'head_contact_2': entry.event.contact_2,
            'participant_name': entry.name,
            'participant_college': entry.college,
            'participant_type': entry.get_type_display(),
            'participant_branch': entry.get_branch_display(),
            'participant_class': entry.get_class_name_display(),
            'participant_phone': entry.phone,
            'participant_email': entry.email,
            'by_name': entry.registered_by.name,
            'by_branch': entry.registered_by.get_branch_display(),
            'by_phone': entry.registered_by.phone,
            'by_email': entry.registered_by.email,
        }
        pdf = render_to_pdf('core/invoice.html', data)
        send_mail(email, MAIL_SUBJECT, MAIL_BODY, pdf)
    except Exception as e:
        print(e)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None


def check_if_exists(data):
    branch = data['branch']
    class_name = data['class_name']
    event = data['event']

    event_instance: Event = get_object_or_404(Event, pk=event)

    if data['type'] == 'INTER' or event_instance.no_limit:
        return False

    current_limit = {
        'FE': {
            'COMP': 3,
            'IT': 1,
            'EXTC': 1,
            'CIVIL': 1,
            'MECH_A': 1,
            'MECH_B': 1,
            'INST': 0,
            'ASH': 0,
            'AIDS': 1,
            'CSE/DS': 1
        },
        'SE': {
            'COMP': 1,
            'IT': 1,
            'EXTC': 1,
            'CIVIL': 1,
            'MECH_A': 1,
            'MECH_B': 1,
            'INST': 0,
            'ASH': 0,
            'AIDS': 1,
            'CSE/DS': 1
        },
        'TE': {
            'COMP': 1,
            'IT': 1,
            'EXTC': 1,
            'CIVIL': 1,
            'MECH_A': 1,
            'MECH_B': 1,
            'INST': 1,
            'ASH': 0,
            'AIDS': 1,
            'CSE/DS': 1
        },
        'BE': {
            'COMP': 2,
            'IT': 2,
            'EXTC': 2,
            'CIVIL': 2,
            'MECH_A': 2,
            'MECH_B': 2,
            'INST': 2,
            'ASH': 0,
            'AIDS': 0,
            'CSE/DS': 0
        },
        'D': {
            'COMP': 1,
            'IT': 1,
            'EXTC': 1,
            'CIVIL': 1,
            'MECH_A': 1,
            'MECH_B': 1,
            'INST': 1,
            'ASH': 1,
            'AIDS': 1,
            'CSE/DS': 1
        },
    }

    current_count = Entry.objects.filter(
        branch=branch, class_name=class_name, event=event).count()
    expected_count = current_limit[class_name][branch]
    return current_count == expected_count
