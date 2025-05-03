from django.shortcuts import render,redirect
from django.views import View
from django.core.mail import send_mail
from paper.forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages
from paper.models.teacher import Teacher
from django.shortcuts import get_object_or_404
from .forms import TeacherUpdateForm


def profile(request):
    # Fetch teacher from session
    teacher_id = request.session.get('teacher')

    if not teacher_id:
        return redirect('login')  # No teacher in session, redirect to login

    try:
        # Get teacher by ID (use the teacher from session)
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        return redirect('signup')  # or wherever you want

    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect after successful update
    else:
        form = TeacherUpdateForm(instance=teacher)

    context = {
        'form': form,
        'teacher': teacher,
    }
    return render(request, 'profile.html', context)


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"New Contact Form Submission from {name}"
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            recipient_email = "utsavipatel0905@gmail.com"  # Replace with your email
            EMAIL_HOST_USER ='hasdkeiqyeurooqv'
            teacher = get_object_or_404(Teacher, id=request.session.get('teacher'))
            try:
                send_mail(
                    subject,
                    body,
                    EMAIL_HOST_USER,  # Sender (must match EMAIL_HOST_USER)
                    [recipient_email],  # List of recipients
                    fail_silently=False,  # Set to False to raise errors
                )
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, f"Failed to send message: {e}")  # Print error

            return render(request, "contact.html", {"teacher": teacher})
    else:
        form = ContactForm()
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher'))

    return render(request, "contact.html", {"form": form,"teacher": teacher})



