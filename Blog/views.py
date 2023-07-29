from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required
from Blog.forms import CommentForm
from .models import Blog,Category, Comment
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib.postgres.search import (SearchHeadline,
                                            SearchQuery,
                                            SearchRank,
                                            SearchVector)
# Create your views here.
class BlogListView(ListView):
    model = Blog
    template_name = "blogs/blogs.html"
    context_object_name="blogs"
    paginate_by = 2
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("category","user")        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.select_related("user")
        return context
    
# @method_decorator(cache_page(60 * 15), name='dispatch')  
class BlogDetailView(DetailView):
    model = Blog
    template_name = "blogs/blog-details.html"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog=self.get_object()
        context["blog"] = blog
        context["categories"]=Category.objects.select_related("user")
        similar_blogs = cache.get(f"similar_blogs_{blog.slug}")
        if similar_blogs is None:
            similar_blogs=blog.category.similar_objects()[:5]
            cache.set(f"similar_blogs_{blog.slug}",similar_blogs)
        context['similar_blogs']=similar_blogs
        context['comments']=Comment.objects.filter(blog=blog).select_related('user')
        return context
    @method_decorator(login_required,name='dispatch')
    def post(self,request,slug,*args, **kwargs):
        if self.request.method =='POST':
            form = CommentForm(self.request.POST)
            if form.is_valid():
                comment=form.cleaned_data['comment']
                try:
                    parent =form.cleaned_data['parent']
                except:
                    parent =None
                new_comment = form.save(commit=False)
                new_comment = Comment(comment=comment,
                                      user = self.request.user,
                                      blog=self.get_object(),
                                      parent=parent,
                                      )
                new_comment.save()
            return redirect(self.request.path_info)
                
    

def search(request):
    results =[]
    if request.method =="GET":
        query = request.GET.get("q")
        search_vector =(
            SearchVector("title",weight="A")
            +SearchVector("content",weight="A")
            +SearchVector("category",weight="B")
        )
        search_query = SearchQuery(query)
        search_headline =SearchHeadline("title",search_query)
        results =(
            Blog.objects.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).
            annotate(headline=search_headline)
            .filter(rank__gte=0.3)
            .order_by("-rank")
            
        )
        results_count= results.count()
        page = request.GET.get("page",1)
        paginator = Paginator(results,10)
        try:
            results=paginator.page(page)
        except PageNotAnInteger:
            results =paginator.page(1)
        except EmptyPage:
            results =paginator.page(paginator.num_pages)
    return render(request,"blogs/search.html",{"results":results,"query":query,"results_count":results_count})


class CategoryListView(ListView):
    model = Blog
    template_name = "blogs/blog-category.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category,slug=self.kwargs.get("slug"))
        blogs = Blog.objects.filter(category=category).select_related('user')
        context["blogs"] =blogs 
        page_num = self.request.GET.get("page", 1)
        paginator = Paginator(blogs, 6)
        try:
            blogs = paginator.page(page_num)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        context = {
            "blogs": blogs,
        }
        return context
    
