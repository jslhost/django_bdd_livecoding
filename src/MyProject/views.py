from django.shortcuts import render
from MyProject.forms import BlogPostForm

def blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            form = BlogPostForm()
    else:
        form = BlogPostForm()

    

    return render(request, "blog_post.html", {"form": form})