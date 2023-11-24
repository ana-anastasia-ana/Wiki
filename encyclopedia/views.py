from random import choice

from django.shortcuts import render, redirect
from markdown2 import markdown

from . import util


def index(request):
    # Given: Home page
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    # TODO: Render a page that displays the contents of that encyclopedia entry
    content = util.get_entry(title.strip())
    """ If an entry is requested that does NOT exist, 
    the user should be presented with an error page 
    indicating that their requested page was not found. """ 
    if content is None:
        content = "<h1>Error: Page Not Found</h1>"
    """  If the entry does exist, 
    the user should be presented with a page that displays the content of the entry. 
    The title of the page should include the name of the entry. """ 
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {"title": title, "entry": content})


def search(request):
    # TODO: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry
    q = request.POST.get('q').strip()
    """ If the query matches the name of an encyclopedia entry, 
    the user should be redirected to that entry’s page. """ 
    if q in util.list_entries():
        return redirect("entry", title=q)
    """ If the query does NOT match the name of an encyclopedia entry, 
    the user should instead be taken to a search results page that 
    displays a list of all encyclopedia entries that have the query as a substring. 
    For example, if the search query were ytho, 
    then Python should appear in the search results. """ 
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})
    """ Clicking on any of the entry names on the search results page 
    should take the user to that entry's page. """ 


def new(request):
    # TODO: Clicking “Create New Page” in the sidebar should take the user to a page 
    # where they can create a new encyclopedia entry.
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title in util.list_entries():
            return render(request, "encyclopedia/new.html", {"error": "Page already exists!"})
            """ When the page is saved, 
            if an encyclopedia entry already exists with the provided title, 
            the user should be presented with an error message. """ 
        elif title == "" or content == "":
            return render(request, "encyclopedia/new.html", {"error": "Title and content are required!"})
        util.save_entry(title, content)
        return redirect("entry", title=title)
        """ Otherwise, the encyclopedia entry should be saved to disk, 
        and the user should be taken to the new entry's page. """ 
    return render(request, "encyclopedia/new.html")


def edit(request, title):
    # TODO: On each entry page, the user should be able to click a link to be taken to a page 
    # where the user can edit that entry’s Markdown content in a textarea.
    content = util.get_entry(title.strip())
    """ Check if entry with this title exists """
    if content is None:
        return render(request, "encyclopedia/edit.html", {'error': "Page Not Found"})
    """ When form is submitted, 
    update entry with new content 
    and redirect to entry page """
    if request.method == "GET":
        content = request.GET.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html",
                          {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    """ Load entry title and content """ 
    return render(request, "encyclopedia/edit.html", {
        'title': title, 'content': content
        })


def random(request):
    # TODO: Clicking “Random Page” in the sidebar should 
    # take user to a random encyclopedia entry.
    entries = util.list_entries()
    return redirect("entry", title=choice(entries))
