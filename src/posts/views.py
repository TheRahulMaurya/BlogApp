
# from urllib import quote_plus     #for share_string
from django.shortcuts import render , get_object_or_404 ,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.db.models import Q
from django.contrib import messages

# Create your views here.
from .models import post

from .forms import PostForm 

def post_home(request):
	return HttpResponse("<h1>hello</h1>")

def create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"created successfully")
		return HttpResponseRedirect(instance.get_absolute_url())

	
		# if reuest.methode=="POST":
		# 	print "title" + request.POST.get("content")
		# 	print request.POST.get("content")
		# 	# post.objects.create(title=title)
	context={
	"title":"form",
	"form":form,
	}
	return render(request,"form_model.html",context)


def read(request,id):
	instance=get_object_or_404(post,id=id)
	# share_string=quote_plus(instance.content)
	context={
			"title":"User",
			"instance" : instance,
			# "share_string":share_string,
		}

	# if request.user.is_authenticated():
	# 	context={
	# 		"title":"Valid User"
	# 	}
	# else:
	# 	context={
	# 		"title":"Invalid User"
	# 	}
	return render(request,"post_list.html",context)


def update(request,id):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(post,id=id)
	form=PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"updated successfully")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context={
	"title":"form",
	"instance":instance,
	"form":form,
	}

	return render(request,"form_model.html",context)

def delete(request,id):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(post,id=id)
	instance.delete()
	messages.success(request,"Deleted Successfully")
	return redirect("/posts/list")



def list(request):
	# queryset=post.objects.all()
	queryset_list=post.objects.all()
	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
	page_request_var="page"
	page = request.GET.get(page_request_var)
	try:
		instance = paginator.page(page)
	except PageNotAnInteger:
    	#if page is not an integer,deliver first page
		instance = paginator.page(1)
	except EmptyPage:
    	# if page is out of range(e.g 9999),deliver last page of result
		paginator.page(paginator.num_pages)

	context={
			"title":"User",
			"object_list" : instance,
			"page_request_var":page_request_var,
		}

	# if request.user.is_authenticated():
	# 	context={
	# 		"title":"Valid User"
	# 	}
	# else:
	# 	context={
	# 		"title":"Invalid User"
	# 	}
	return render(request,"index.html",context)
	


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def listing(request):
    contact_list = Contacts.objects.all()
    paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'list.html', {'contacts': contacts})


