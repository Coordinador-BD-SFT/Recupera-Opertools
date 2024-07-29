from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ReporteWhatsapp
from .forms import UploadChatBaseForm

# Create your views here.


def reportes(request):
    reportes = ReporteWhatsapp.objects.all()
    # return HttpResponse(f'Solicitud exitosa; Reportes:\n {reportes}')
    # reporte = ReporteWhatsapp.objects.get(pk=2)
    # file = reporte.chats.

    return render(
        request,
        'reportes.html',
        context={'reportes': reportes}
    )


def ReporteWspForm(request):
    if request.method == 'POST':
        form = UploadChatBaseForm(request.POST, request.FILES)
        if form.is_valid():
            print('Petition processed successfully!')
            form.save()
            return redirect('reportes')
    else:
        form = UploadChatBaseForm()
        return render(request, 'crear_reporte.html', context={'form': form})
