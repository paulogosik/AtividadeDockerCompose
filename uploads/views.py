from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ArquivoForm
from .models import Arquivo


@require_http_methods(["GET", "POST", "HEAD"])
def index(request):
    if request.method == "POST":
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.save(commit=False)
            arquivo.nome = form.cleaned_data["arquivo"].name
            arquivo.save()
            # Redirecionar evita repetir o upload ao atualizar a página.
            return redirect("index")
    else:
        form = ArquivoForm()

    return render(
        request,
        "uploads/index.html",
        {"form": form, "arquivos": Arquivo.objects.all()},
    )
