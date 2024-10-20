from django.shortcuts import render, redirect
from . import util
import markdown2
import random

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {"entries": entries})

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested entry was not found."
        })
    else:
        html_content = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()

    query_lower = query.lower()

    exact_matches = [entry for entry in entries if entry.lower() == query_lower]

    if exact_matches:
        return entry(request, exact_matches[0])

    partial_matches = [entry for entry in entries if query_lower in entry.lower()]

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": partial_matches
    })

def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/create_page.html",{
                "error_message": "An entry with this title already exists."
            })
        util.save_entry(title, content)
        
        return redirect('entry', title=title)
    
    return render(request, "encyclopedia/create_page.html")

def edit_page(request, title):
    entry_content = util.get_entry(title)

    if entry_content is None:
        return render(request, "encyclopedia/error.html", {"message": "The requested entry does not exist."})
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entry', title=title) 
    return render(request, "encyclopedia/edit_page.html",{"title": title, "content": entry_content})

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)
            
        