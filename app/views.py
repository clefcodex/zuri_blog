from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from .forms import CommentForm
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class BlogListView(ListView):
	model = Post
	template_name = 'home.html'


# class BlogDetailView(DetailView):
# 	model = Post
# 	template_name = 'post_detail.html'
# 	comments = post.comments.all()



def blog_detail_view(request, pk):
	try:
		post = Post.objects.get(pk=pk)
		comments = post.comments.all()
	except Post.DoesNotExist:
		raise Http404

	
	cf = CommentForm(request.POST or None)
	
	if cf.is_valid():
		content = request.POST.get('content')
		comment = Comment.objects.create(post = post, user = request.user, content = content)
		comment.save()
		return redirect(post.get_absolute_url())
	

	context = {"post": post, "comments": comments, 'comment_form': cf}
	return render(request, "post_detail.html", context)



class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'post_new.html'
	fields = ['title', 'author', 'body']


class BlogUpdateView(UpdateView):
	model = Post
	template_name = 'post_edit.html'
	fields = ['title', 'body']


class BlogDeleteView(DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('home')


