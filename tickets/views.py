from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Ticket
from .forms import TicketForm

@login_required
def portal_home(request):
    is_staff = request.user.is_staff

    # Agents see all tickets; customers only see their own submissions
    if is_staff:
        tickets = Ticket.objects.all().order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(customer=request.user).order_by('-created_at')

    # Handle ticket submission
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.customer = request.user
            new_ticket.save()
            return redirect('portal_home')
    else:
        form = TicketForm()

    # Calculate operational metrics
    stats = {
        'total': Ticket.objects.count(),
        'pending': Ticket.objects.filter(status='Pending').count(),
        'in_progress': Ticket.objects.filter(status='In Progress').count(),
        'resolved': Ticket.objects.filter(status='Resolved').count(),
    }

    context = {
        'tickets': tickets,
        'form': form,
        'stats': stats,
        'is_staff': is_staff,
    }
    return render(request, 'tickets/portal.html', context)

@login_required
@login_required
@require_POST
def update_status(request, ticket_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    ticket = get_object_or_404(Ticket, id=ticket_id)
    new_status = request.POST.get('status')
    
    if new_status in ['Pending', 'In Progress', 'Resolved']:
        ticket.status = new_status
        ticket.save()

        # Recalculate HUD counts
        total = Ticket.objects.count()
        pending = Ticket.objects.filter(status='Pending').count()
        in_progress = Ticket.objects.filter(status='In Progress').count()
        resolved = Ticket.objects.filter(status='Resolved').count()

        return JsonResponse({
            'success': True,
            'status': ticket.status,
            'counts': {
                'total': total,
                'pending': pending,
                'in_progress': in_progress,
                'resolved': resolved,
            }
        })

    return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)