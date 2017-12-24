from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save  #for slug
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

class PostManager(models.Manager):
	def all(self, *args,**kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)

class post(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title=models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image=models.ImageField(upload_to=upload_location,
		null=True,
		blank=True,
		width_field="width_field",
		height_field="height_field"
		)
	height_field=models.IntegerField(default=0)
	width_field=models.IntegerField(default=0)
	content=models.TextField()
	draft=models.BooleanField(default=False)
	publish=models.DateField(auto_now=False,auto_now_add=False)
	update=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)


	def __unicode__(self):
		return self.title;


	def __str__(self):
		return self.title;

	def get_absolute_url(self):
		return reverse("posts:detail",kwargs={"id":self.id})
		#return "/posts/%s/" %(self.slug)

	class Meta:
		ordering=["-timestamp","-update"]


	objects=PostManager()	

def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	queryset = post.objects.filter(slug=slug).order_by("-id")
	exists=queryset.exists()
	if exists:
		new_slug = "%s-%s" %(slug,queryset.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug


def pre_save_post_reciever(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
	#Tesla item 1 -> tesla-item-1


pre_save.connect(pre_save_post_reciever,sender=post)