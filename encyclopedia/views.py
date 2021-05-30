from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import secrets
import markdown2

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label = "title")
    content = forms.CharField(label = "content", widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(label = "content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.list_entries()
    if title not in entries:
        return render(request, "encyclopedia/error.html", {
            "error_case": "Error-Page not found",
            "error_message": f"Error : '{ title }' was not found"
        })
    else:
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

def search(request):
    entries = util.list_entries()
    if request.method == "POST":
        # Get a title value from form
        title = request.POST['q']
        if title not in entries:
            substring_result = []
            for entry in entries:
                if title.lower() in entry.lower():
                    substring_result.append(entry)
            if not substring_result:
                return render(request, "encyclopedia/error.html", {
                    "error_case": "Error-No page found",
                    "error_message": "No page found for your search"
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "title": title,
                    "entries": substring_result
                })
        else:
            content = markdown2.markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })

def new_page(request):
    if request.method == "POST":
        entries = util.list_entries()
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # If title already exists, shows error
            if title in entries:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error_message": "The title has been used already."
                })
            # If it is new title, save new entry to entries directory
            util.save_entry(title, content)
            content = markdown2.markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
        # Form is invalid, show error
        return render(request, "encyclopedia/error.html", {
            "error_case": "Error-Form is invalid",
            "error_message": "Error : Form is invalid"
        })
    # Render blank new_page for user
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm()
    })

def edit_page(request, title):
    # Change content of entry file when user "POST"
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            content = markdown2.markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
        # Form is invalid, show error
        return render(request, "encyclopedia/error.html", {
            "error_case": "Error-Form is invalid",
            "error_message": "Error : Form is invalid"
        })
    # Get content by title
    content = util.get_entry(title)
    # If title exists, render edit_page with prepopulated form
    if content != None:
        form = EditPageForm(initial={"content":content})
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "form": form
        })
    # If title does not exists, show error-Page not found
    return render(request, "encyclopedia/error.html", {
        "error_case": "Error-Page not found",
        "error_message": f"Error : '{ title }' was not found"
    })

def random(request):
    # Get list of all titles
    entries = util.list_entries()
    # Secretly random one title
    title = secrets.choice(entries)
    # Render the title
    content = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })