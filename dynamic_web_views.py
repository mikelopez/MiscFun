# Author Marcos Lopez
# Custom crud for Sciweb420 websites (deprecated)
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import loader
import settings as SETTING

from webAdmin.models import *

from msgs import *
import CustomSettings as C_SETTING

def get_get(req):
	try:
		msg = req.GET.get('msg','n')
	except ValueError:
		msg	= 'n'
	try:
		notify = req.GET.get('notify','n')
	except ValueError:
		notify	= 'n'

	try:
		orderby = req.GET.get('orderby','n')
	except ValueError:
		orderby	= 'n'

	try:
		page = int(req.GET.get('page','1'))
	except ValueError:
		page	= 1

	return {'msg':msg,
		'notify':notify,
		'orderby':orderby,
		'page':page,
	}


def paginate_urls(pag_obj, order_by):
	if pag_obj.has_next():
		if order_by == 'n':
			nexturl = '?page=%s' % (pag_obj.next_page_number())
		else:
			nexturl = '?orderby=%s&page=%s' % (order_by,pag_obj.next_page_number())

	else:
		nexturl = '#'
	#
	if pag_obj.has_previous():
		if order_by == 'n':
			prevurl = '?page=%s' % (pag_obj.previous_page_number())
		else:
			prevurl = '?orderby=%s&page=%s' % (order_by,pag_obj.previous_page_number())
	else:
		prevurl = '#'

	return {
		'nexturl':nexturl,
		'prevurl':prevurl,
	}



@login_required
def index(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		return render_to_response('crud/test.html', {
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def webadmin(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		return render_to_response('crud/webadmin.html', {
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def productsadmin(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		return render_to_response('crud/productsadmin.html', {
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def content_admin(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		return render_to_response('crud/contentadmin.html', {
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)


@login_required
def websites(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(Websites.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(Websites.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			websites = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			websites = paginator.page(paginator.num_pages)

		pageurls = paginate_urls(websites, gets['orderby'])

		return render_to_response('crud/websites.html', {
				'websites':websites,'page':gets['page'],
				'msg':gets['msg'],'notify':gets['notify'],
				'nexturl':pageurls['nexturl'],'prevurl':pageurls['prevurl'],
			}
		)


@login_required
def new_website(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_website.html', {
				'website_categories':Categories.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)


@login_required
def new_website_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = WebsitesForm(request.POST)
			new_site = f.save()
			msg = web_site_added
			return HttpResponseRedirect('/crud/websites/?notify=%s' % (msg)) 
		except ValueError:
			msg = web_site_error
			return HttpResponseRedirect('/crud/new_website/?msg=%s' % (msg))

	



@login_required
def edit_website(request, websiteid):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				website = Websites.objects.get(pk=int(websiteid))
			except:
				msg=web_site_edit_not_found
				return HttpResponseRedirect('/crud/websites/?msg=%s' % (msg))
			gets = get_get(request)
			f = WebsitesForm(instance=website)
			return render_to_response('crud/edit_website.html', {
				'website':website,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				website = Websites.objects.get(pk=int(websiteid))
			except:
				msg=web_site_edit_not_found
				return HttpResponseRedirect('/crud/websites/?msg=%s' % (msg))

			formset = WebsitesForm(request.POST, instance=website)
			if formset.is_valid():
				formset.save()
				msg=web_site_edit_ok
				return HttpResponseRedirect('/crud/websites/?notify=%s' % (msg))

			else:
				msg = web_site_edit_not_found
				return HttpResponseRedirect('/crud/websites/?msg=%s' % (msg))
		
	


@login_required
def website_categories(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(Categories.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(Categories.objects.all().orderby(gets['orderby']), C_SETTING.paginate_count)

		try:
			website_categories = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			website_categories = paginator.page(paginator.num_pages)
		
		page_urls = paginate_urls(website_categories, gets['orderby'])

		return render_to_response('crud/website_categories.html', {
				'website_categories':website_categories,'page':gets['page'],
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)


@login_required
def website_categories_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = CategoriesForm(request.POST)
			new_f = f.save()
			msg = web_cat_added
			return HttpResponseRedirect('/crud/website_categories/?notify=%s' % (msg))
		except ValueError:
			msg = web_cat_error
			return HttpResponseRedirect('/crud/website_categories/?msg=%s' % (msg))


@login_required
def edit_website_categories(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				cat = Categories.objects.get(pk=int(id))
			except:
				msg=web_cat_edit_not_found
				return HttpResponseRedirect('/crud/website_categories/?msg=%s' % (msg))

			gets = get_get(request)
			f = CategoriesForm(instance=cat)
			return render_to_response('crud/edit_website_categories.html', {
				'cat':cat,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				cat = Categories.objects.get(pk=int(id))
			except:
				msg=web_cat_edit_not_found
				return HttpResponseRedirect('/crud/website_categories/?msg=%s' % (msg))

			formset = CategoriesForm(request.POST, instance=cat)
			if formset.is_valid():
				formset.save()
				msg=web_cat_edit_ok
				return HttpResponseRedirect('/crud/website_categories/?notify=%s' % (msg))

			else:
				msg = web_cat_edit_not_found
				return HttpResponseRedirect('/crud/website_categories/?msg=%s' % (msg))





@login_required
def website_pages(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(SitePages.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(SitePages.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			website_pages = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			website_pages = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(website_pages, gets['orderby'])
		
		return render_to_response('crud/website_sitepages.html', {
				'page':gets['page'],'website_pages':website_pages,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_website_page(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_website_page.html', {
				'website_categories':Categories.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				'websites':Websites.objects.all(),
				'siteproperties':SiteProperties.objects.all(),
				'templates':Templates.objects.all(),
				'linkcategories':CategoryAdvertiser.objects.all(),
				'contentcategories':CategoryParent.objects.all()
			}
		)

@login_required
def new_website_page_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = SitePagesForm(request.POST)
			new_f = f.save()
			msg = web_page_added
			return HttpResponseRedirect('/crud/website_pages/?notify=%s' % (msg))
		except ValueError:
			msg = web_page_error
			return HttpResponseRedirect('/crud/website_pages/?msg=%s' % (msg))

		return render_to_response('crud/website_sitepages.html', {
				'website_categories':Categories.objects.all(),

			}
		)



@login_required
def edit_website_page(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				pg = SitePages.objects.get(pk=int(id))
			except:
				msg=web_page_edit_not_found
				return HttpResponseRedirect('/crud/website_pages/?msg=%s' % (msg))

			gets = get_get(request)
			f = SitePagesForm(instance=pg)
			return render_to_response('crud/edit_website_page.html', {
				'pg':pg,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				pg = SitePages.objects.get(pk=int(id))
			except:
				msg=web_page_edit_not_found
				return HttpResponseRedirect('/crud/website_pages/?msg=%s' % (msg))
			formset = SitePagesForm(request.POST, instance=pg)
			if formset.is_valid():
				formset.save()
				msg=web_cat_edit_ok
				return HttpResponseRedirect('/crud/website_pages/?notify=%s' % (msg))

			else:
				msg = web_cat_edit_not_found
				return HttpResponseRedirect('/crud/website_pages/?msg=%s' % (msg))





@login_required
def website_properties(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(SiteProperties.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(SiteProperties.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			website_properties = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			website_properties = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(website_properties, gets['orderby'])

		return render_to_response('crud/website_properties.html', {
				'page':gets['page'],'website_properties':website_properties,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				'websites':Websites.objects.all(),
				'site_themes':SiteThemes.objects.all(),
			}
		)


@login_required
def new_website_properties(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_website_properties.html', {
				'website_categories':Categories.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				'websites':Websites.objects.all(),
				'site_themes':SiteThemes.objects.all(),
			}
		)


@login_required()
def website_properties_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = SitePropertiesForm(request.POST)
			new_f = f.save()
			msg = web_properties_added
			return HttpResponseRedirect('/crud/website_properties/?notify=%s' % (msg))
		except ValueError:
			msg = web_properties_error
			return HttpResponseRedirect('/crud/website_properties/?msg=%s' % (msg))


@login_required
def edit_website_properties(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				sp = SiteProperties.objects.get(pk=int(id))
			except:
				msg=web_properties_edit_not_found
				return HttpResponseRedirect('/crud/website_properties/?msg=%s' % (msg))

			gets = get_get(request)
			f = SitePropertiesForm(instance=sp)
			return render_to_response('crud/edit_website_properties.html', {
				'sp':sp,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				sp = SiteProperties.objects.get(pk=int(id))
			except:
				msg=web_properties_edit_not_found
				return HttpResponseRedirect('/crud/website_properties/?msg=%s' % (msg))
			formset = SitePropertiesForm(request.POST, instance=sp)
			if formset.is_valid():
				formset.save()
				msg=web_properties_edit_ok
				return HttpResponseRedirect('/crud/website_properties/?notify=%s' % (msg))

			else:
				msg = web_properties_edit_not_found
				return HttpResponseRedirect('/crud/website_properties/?msg=%s' % (msg))







@login_required()
def website_links(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(SiteLinks.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(SiteLinks.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			website_links = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			website_links = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(website_links, gets['orderby'])

		return render_to_response('crud/website_sitelinks.html', {
				'page':gets['page'],'website_links':website_links,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				'websites':Websites.objects.all(),

			}
		)

@login_required
def new_website_links(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_website_link.html', {

				'msg':gets['msg'],'notify':gets['notify'],
				'websites':Websites.objects.all(),
			}
		)

@login_required()
def website_links_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = SiteLinksForm(request.POST)
			new_f = f.save()
			msg = web_links_added
			return HttpResponseRedirect('/crud/website_links/?notify=%s' % (msg))
		except ValueError:
			msg = web_links_error
			return HttpResponseRedirect('/crud/website_links/?msg=%s' % (msg))


@login_required
def edit_website_link(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				sp = SiteLinks.objects.get(pk=int(id))
			except:
				msg=web_links_edit_not_found
				return HttpResponseRedirect('/crud/website_links/?msg=%s' % (msg))

			gets = get_get(request)
			f = SiteLinksForm(instance=sp)
			return render_to_response('crud/edit_website_link.html', {
				'sl':sp,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				sp = SiteLinks.objects.get(pk=int(id))
			except:
				msg=web_links_edit_not_found
				return HttpResponseRedirect('/crud/website_links/?msg=%s' % (msg))
			formset = SiteLinksForm(request.POST, instance=sp)
			if formset.is_valid():
				formset.save()
				msg=web_links_edit_ok
				return HttpResponseRedirect('/crud/website_links/?notify=%s' % (msg))

			else:
				msg = web_links_edit_not_found
				return HttpResponseRedirect('/crud/website_links/?msg=%s' % (msg))


@login_required()
def templates(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(Templates.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(Templates.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			templ = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			templ = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(templ, gets['orderby'])

		return render_to_response('crud/templates.html', {
				'page':gets['page'],'templates':templ,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				

			}
		)




@login_required
def new_template(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_template.html', {

				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)

@login_required()
def new_template_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = TemplatesForm(request.POST, request.FILES)
			new_f = f.save()
			msg = web_templates_added
			return HttpResponseRedirect('/crud/templates/?notify=%s' % (msg))
		except ValueError:
			msg = web_templates_error
			return HttpResponseRedirect('/crud/templates/?msg=%s' % (msg))



@login_required
def edit_template(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				cs = Templates.objects.get(pk=int(id))
			except:
				msg=web_templates_edit_not_found
				return HttpResponseRedirect('/crud/templates/?msg=%s' % (msg))

			gets = get_get(request)
			f = TemplatesForm(instance=cs)
			return render_to_response('crud/edit_templates.html', {
				'template':cs,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				cs = Templates.objects.get(pk=int(id))
			except:
				msg=web_templates_edit_not_found
				return HttpResponseRedirect('/crud/templates/?msg=%s' % (msg))
			formset = TemplatesForm(request.POST, request.FILES, instance=cs)
			if formset.is_valid():
				if request.POST['delete_template'] == 'y':

					dirs = '%s' % (cs.image)
					try:
						os.system('rm %s' % (dirs))
					except:
						pass


				formset.save()
				msg=web_templates_edit_ok
				return HttpResponseRedirect('/crud/templates/?notify=%s' % (msg))

			else:
				msg = web_templates_edit_not_found
				return HttpResponseRedirect('/crud/templates/?msg=%s' % (msg))




#
@login_required()
def webimages(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(Images.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(Images.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			templ = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			templ = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(templ, gets['orderby'])

		return render_to_response('crud/images.html', {
				'page':gets['page'],'images':templ,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				

			}
		)


@login_required
def new_images(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_images.html', {

				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)

@login_required()
def new_images_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = ImagesForm(request.POST, request.FILES)
			new_f = f.save()
			msg = web_images_added
			return HttpResponseRedirect('/crud/webimages/?notify=%s' % (msg))
		except ValueError:
			msg = web_images_error
			return HttpResponseRedirect('/crud/webimages/?msg=%s' % (msg))



@login_required
def edit_images(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				cs = Images.objects.get(pk=int(id))
			except:
				msg=web_images_edit_not_found
				return HttpResponseRedirect('/crud/webimages/?msg=%s' % (msg))

			gets = get_get(request)
			f = ImagesForm(instance=cs)
			return render_to_response('crud/edit_images.html', {
				'image':cs,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				cs = Images.objects.get(pk=int(id))
			except:
				msg=web_images_edit_not_found
				return HttpResponseRedirect('/crud/webimages/?msg=%s' % (msg))
			formset = ImagesForm(request.POST, request.FILES, instance=cs)
			if formset.is_valid():
				if request.POST['delete_image'] == 'y':

					dirs = '%s' % (cs.image)
					try:
						os.system('rm %s' % (dirs))
					except:
						pass


				formset.save()
				msg=web_images_edit_ok
				return HttpResponseRedirect('/crud/webimages/?notify=%s' % (msg))

			else:
				msg = web_images_edit_not_found
				return HttpResponseRedirect('/crud/webimages/?msg=%s' % (msg))



#



@login_required()
def cssoverrides(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(CSSOverrides.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(CSSOverrides.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			cs = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			cs = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(cs, gets['orderby'])

		return render_to_response('crud/cssoverrides.html', {
				'page':gets['page'],'cs':cs,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				

			}
		)


@login_required
def new_cssoverrides(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_cssoverrides.html', {
				'websites':Websites.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)

	
	
@login_required()
def new_cssoverrides_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = CSSOverridesForm(request.POST, request.FILES)
			new_f = f.save()
			msg = css_overrides_added
			return HttpResponseRedirect('/crud/cssoverrides/?notify=%s' % (msg))
		except ValueError:
			msg = css_overrides_error
			return HttpResponseRedirect('/crud/cssoverrides/?msg=%s' % (msg))


@login_required
def edit_cssoverrides(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				cs = CSSOverrides.objects.get(pk=int(id))
			except:
				msg=css_overrides_edit_not_found
				return HttpResponseRedirect('/crud/cssoverrides/?msg=%s' % (msg))

			gets = get_get(request)
			f = CSSOverridesForm(instance=cs)
			return render_to_response('crud/edit_cssoverrides.html', {
				'cs':cs,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				cs = CSSOverrides.objects.get(pk=int(id))
			except:
				msg=css_overrides_edit_not_found
				return HttpResponseRedirect('/crud/cssoverrides/?msg=%s' % (msg))
			formset = CSSOverridesForm(request.POST, instance=cs)
			if formset.is_valid():
				formset.save()
				msg=css_overrides_edit_ok
				return HttpResponseRedirect('/crud/cssoverrides/?notify=%s' % (msg))

			else:
				msg = css_overrides_edit_not_found
				return HttpResponseRedirect('/crud/cssoverrides/?msg=%s' % (msg))



@login_required()
def jsoverrides(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(JSOverrides.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(JSOverrides.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			js = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			js = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(js, gets['orderby'])

		return render_to_response('crud/jsoverrides.html', {
				'page':gets['page'],'js':js,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				

			}
		)


@login_required
def new_jsoverrides(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_jsoverrides.html', {
				'websites':Websites.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)

	
	
@login_required()
def new_jsoverrides_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = JSOverridesForm(request.POST, request.FILES)
			new_f = f.save()
			msg = js_overrides_added
			return HttpResponseRedirect('/crud/jsoverrides/?notify=%s' % (msg))
		except ValueError:
			msg = js_overrides_error
			return HttpResponseRedirect('/crud/jsoverrides/?msg=%s' % (msg))


@login_required
def edit_jsoverrides(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				js = JSOverrides.objects.get(pk=int(id))
			except:
				msg=css_overrides_edit_not_found
				return HttpResponseRedirect('/crud/jsoverrides/?msg=%s' % (msg))

			gets = get_get(request)
			f = JSOverridesForm(instance=js)
			return render_to_response('crud/edit_jsoverrides.html', {
				'js':js,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				js = JSOverrides.objects.get(pk=int(id))
			except:
				msg=js_overrides_edit_not_found
				return HttpResponseRedirect('/crud/jsoverrides/?msg=%s' % (msg))
			formset = JSOverridesForm(request.POST, instance=js)
			if formset.is_valid():
				formset.save()
				msg=js_overrides_edit_ok
				return HttpResponseRedirect('/crud/jsoverrides/?notify=%s' % (msg))

			else:
				msg = js_overrides_edit_not_found
				return HttpResponseRedirect('/crud/jsoverrides/?msg=%s' % (msg))


@login_required()
def sitevisits(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(SiteVisits.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(SiteVisitss.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			sv = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			sv = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(sv, gets['orderby'])

		return render_to_response('crud/sitevisits.html', {
				'page':gets['page'],'sv':sv,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				

			}
		)

@login_required
def weblinkprofiles(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(WebLinksProfile.objects.all(), 20)
		else:
			paginator = Paginator(WebLinksProfile.objects.all().order_by(gets['orderby']), 20)

		try:
			weblink_profiles = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			weblink_profiles = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(weblink_profiles, gets['orderby'])

		return render_to_response('crud/weblinkprofiles.html', {
				'page':gets['page'],'weblink_profiles':weblink_profiles,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required
def new_weblinkprofiles(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_weblinkprofiles.html', {
			'links':LinksProfile.objects.all(),
			'sitepage':SitePages.objects.all(),
			'site':Websites.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_weblinkprofiles_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = WebLinksProfileForm(request.POST, request.FILES)
			new_f = f.save()
			msg = weblink_profiles_added
			return HttpResponseRedirect('/crud/jsoverrides/?notify=%s' % (msg))
		except ValueError:
			msg = weblink_profiles_error
			return HttpResponseRedirect('/crud/jsoverrides/?msg=%s' % (msg))


@login_required
def edit_weblinkprofiles(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				weblink = WebLinksProfile.objects.get(pk=int(id))
			except:
				msg=weblink_profiles_edit_not_found
				return HttpResponseRedirect('/crud/weblinkprofiles/?msg=%s' % (msg))

			gets = get_get(request)
			f = WebLinksProfileForm(instance=weblink)
			return render_to_response('crud/edit_weblinkprofiles.html', {
				'weblink_profile':weblink,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				weblink = WebLinksProfile.objects.get(pk=int(id))
			except:
				msg=weblink_profiles_edit_not_found
				return HttpResponseRedirect('/crud/weblinkprofiles/?msg=%s' % (msg))
			formset = WebLinkProfilesForm(request.POST, instance=weblink)
			if formset.is_valid():
				formset.save()
				msg=weblink_profiles_edit_ok
				return HttpResponseRedirect('/crud/weblinkprofiles/?notify=%s' % (msg))

			else:
				msg = weblink_profiles_edit_not_found
				return HttpResponseRedirect('/crud/weblinkprofiles/?msg=%s' % (msg))




@login_required
def webcontentprofiles(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(WebContentProfile.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(WebContentProfile.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			webcontent_profiles = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			webcontent_profiles = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(webcontent_profiles, gets['orderby'])

		return render_to_response('crud/webcontentprofiles.html', {
				'page':gets['page'],'webcontent_profiles':webcontent_profiles,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required
def new_webcontentprofiles(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_webcontentprofiles.html', {
			'content':ContentProfile.objects.all(),
			'sitepage':SitePages.objects.all(),
			'site':Websites.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_webcontentprofiles_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = WebContentProfileForm(request.POST, request.FILES)
			new_f = f.save()
			msg = webcontent_profiles_added
			return HttpResponseRedirect('/crud/webcontentprofiles/?notify=%s' % (msg))
		except ValueError:
			msg = webcontent_profiles_error
			return HttpResponseRedirect('/crud/webcontentprofiles/?msg=%s' % (msg))


@login_required
def edit_webcontentprofiles(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				webcontent = WebContentProfile.objects.get(pk=int(id))
			except:
				msg=webcontent_profiles_edit_not_found
				return HttpResponseRedirect('/crud/webcontentprofiles/?msg=%s' % (msg))

			gets = get_get(request)
			f = WebContentProfileForm(instance=webcontent)
			return render_to_response('crud/edit_webcontentprofiles.html', {
				'webcontent_profile':webcontent,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				webcontent = WebContentProfile.objects.get(pk=int(id))
			except:
				msg=webcontent_profiles_edit_not_found
				return HttpResponseRedirect('/crud/webcontentprofiles/?msg=%s' % (msg))
			formset = WebContentProfileForm(request.POST, instance=webcontent)
			if formset.is_valid():
				formset.save()
				msg=webcontent_profiles_edit_ok
				return HttpResponseRedirect('/crud/webcontentprofiles/?notify=%s' % (msg))

			else:
				msg = webcontent_profiles_edit_not_found
				return HttpResponseRedirect('/crud/webcontentprofiles/?msg=%s' % (msg))

# end webadmin


@login_required
def advertiser_networks(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(Networks.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(Networks.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			advnetworks = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			advnetworks = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(advnetworks, gets['orderby'])

		return render_to_response('crud/advertiser_networks.html', {
				'page':gets['page'],'advnetworks':advnetworks,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)

@login_required
def new_advertiser_networks(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_advertiser_networks.html', {
				
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_advertiser_networks_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = NetworksForm(request.POST, request.FILES)
			new_f = f.save()
			msg = advertiser_networks_added
			return HttpResponseRedirect('/crud/advertiser_networks/?notify=%s' % (msg))
		except ValueError:
			msg = advertiser_networks_error
			return HttpResponseRedirect('/crud/advertiser_networks/?msg=%s' % (msg))


@login_required
def edit_advertiser_networks(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				netw = Networks.objects.get(pk=int(id))
			except:
				msg=advertiser_networks_edit_not_found
				return HttpResponseRedirect('/crud/advertiser_networks/?msg=%s' % (msg))

			gets = get_get(request)
			f = NetworksForm(instance=netw)
			return render_to_response('crud/edit_advertiser_networks.html', {
				'advnetwork':netw,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				netw = Networks.objects.get(pk=int(id))
			except:
				msg=advertiser_networks_edit_not_found
				return HttpResponseRedirect('/crud/advertiser_networks/?msg=%s' % (msg))
			formset = NetworksForm(request.POST, instance=netw)
			if formset.is_valid():
				formset.save()
				msg=advertiser_networks_edit_ok
				return HttpResponseRedirect('/crud/advertiser_networks/?notify=%s' % (msg))

			else:
				msg = advertiser_networks_edit_not_found
				return HttpResponseRedirect('/crud/advertiser_networks/?msg=%s' % (msg))


@login_required
def advertiser(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(Advertiser.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(Advertiser.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			ad = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			ad = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(ad, gets['orderby'])

		return render_to_response('crud/advertiser.html', {
				'categoryadvertiser':CategoryAdvertiser.objects.all(),
				'networks':Networks.objects.all(),
				'page':gets['page'],'ad':ad,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_advertiser(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_advertiser.html', {
			'networks':Networks.objects.all(),
			'categoryadvertiser':CategoryAdvertiser.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_advertiser_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = AdvertiserForm(request.POST, request.FILES)
			new_f = f.save()
			msg = advertiser_added
			return HttpResponseRedirect('/crud/advertiser/?notify=%s' % (msg))
		except ValueError:
			msg = advertiser_error
			return HttpResponseRedirect('/crud/advertiser/?msg=%s' % (msg))


@login_required
def edit_advertiser(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				ad = Advertiser.objects.get(pk=int(id))
			except:
				msg=advertiser_edit_not_found
				return HttpResponseRedirect('/crud/advertiser/?msg=%s' % (msg))

			gets = get_get(request)
			f = AdvertiserForm(instance=ad)
			return render_to_response('crud/edit_advertiser.html', {
				'ad':ad,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				ad = Advertiser.objects.get(pk=int(id))
			except:
				msg=advertiser_edit_not_found
				return HttpResponseRedirect('/crud/advertiser/?msg=%s' % (msg))
			formset = AdvertiserForm(request.POST, instance=ad)
			if formset.is_valid():
				formset.save()
				msg=advertiser_edit_ok
				return HttpResponseRedirect('/crud/advertiser/?notify=%s' % (msg))

			else:
				msg = advertiser_edit_not_found
				return HttpResponseRedirect('/crud/advertiser/?msg=%s' % (msg))




# ---

@login_required
def advertiser_categories(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(CategoryAdvertiser.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(CategoryAdvertiser.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			ad = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			ad = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(ad, gets['orderby'])

		return render_to_response('crud/advertiser_categories.html', {
				
				'page':gets['page'],'ad':ad,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_advertiser_categories(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_advertiser_categories.html', {
				
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_advertiser_categories_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = CategoryAdvertiserForm(request.POST, request.FILES)
			new_f = f.save()
			msg = advertiser_categories_added
			return HttpResponseRedirect('/crud/advertiser_categories/?notify=%s' % (msg))
		except ValueError:
			msg = advertiser_categories_error
			return HttpResponseRedirect('/crud/advertiser_categories/?msg=%s' % (msg))


@login_required
def edit_advertiser_categories(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				ad = CategoryAdvertiser.objects.get(pk=int(id))
			except:
				msg=advertiser_categories_edit_not_found
				return HttpResponseRedirect('/crud/advertiser_categories/?msg=%s' % (msg))

			gets = get_get(request)
			f = CategoryAdvertiserForm(instance=ad)
			return render_to_response('crud/edit_advertiser_categories.html', {
				'ad':ad,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				ad = CategoryAdvertiser.objects.get(pk=int(id))
			except:
				msg=advertiser_categories_edit_not_found
				return HttpResponseRedirect('/crud/advertiser_categories/?msg=%s' % (msg))
			formset = CategoryAdvertiserForm(request.POST, instance=ad)
			if formset.is_valid():
				formset.save()
				msg=advertiser_categories_edit_ok
				return HttpResponseRedirect('/crud/advertiser_categories/?notify=%s' % (msg))

			else:
				msg = advertiser_categories_edit_not_found
				return HttpResponseRedirect('/crud/advertiser_categories/?msg=%s' % (msg))



@login_required
def product_categories(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(CategoryLink.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(CategoryLink.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			cat = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			cat = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(cat, gets['orderby'])

		return render_to_response('crud/product_categories.html', {
				
				'page':gets['page'],'cat':cat,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_product_categories(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_product_categories.html', {
			'categoryadvertiser':CategoryAdvertiser.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_product_categories_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = CategoryLinkForm(request.POST, request.FILES)
			new_f = f.save()
			msg = product_categories_added
			return HttpResponseRedirect('/crud/product_categories/?notify=%s' % (msg))
		except ValueError:
			msg = product_categories_error
			return HttpResponseRedirect('/crud/product_categories/?msg=%s' % (msg))



@login_required
def edit_product_categories(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				cat = CategoryLink.objects.get(pk=int(id))
			except:
				msg=product_categories_edit_not_found
				return HttpResponseRedirect('/crud/product_categories/?msg=%s' % (msg))

			gets = get_get(request)
			f = CategoryLinkForm(instance=cat)
			return render_to_response('crud/edit_product_categories.html', {
				'cat':cat,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				cat = CategoryLink.objects.get(pk=int(id))
			except:
				msg=product_categories_edit_not_found
				return HttpResponseRedirect('/crud/product_categories/?msg=%s' % (msg))
			formset = CategoryLinkForm(request.POST, instance=cat)
			if formset.is_valid():
				formset.save()
				msg=product_categories_edit_ok
				return HttpResponseRedirect('/crud/product_categories/?notify=%s' % (msg))

			else:
				msg = product_categories_edit_not_found
				return HttpResponseRedirect('/crud/product_categories/?msg=%s' % (msg))

	


@login_required
def productlinks(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(ProductLinks.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(ProductLinks.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])

		return render_to_response('crud/productlinks.html', {
				
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_productlinks(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_productlinks.html', {
			'advertiser':Advertiser.objects.all(),
			'categorylink':CategoryLink.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_productlinks_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = ProductLinksFormAll(request.POST, request.FILES)
			new_f = f.save()
			msg = productlinks_added
			return HttpResponseRedirect('/crud/productlinks/?notify=%s' % (msg))
		except ValueError:
			msg = productlinks_error
			return HttpResponseRedirect('/crud/productlinks/?msg=%s' % (msg))



@login_required
def edit_productlinks(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				p = ProductLinks.objects.get(pk=int(id))
			except:
				msg=productlinks_edit_not_found
				return HttpResponseRedirect('/crud/productlinks/?msg=%s' % (msg))

			gets = get_get(request)
			f = ProductLinksForm(instance=p)
			return render_to_response('crud/edit_productlinks.html', {
				'p':p,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				p = ProductLinks.objects.get(pk=int(id))
			except:
				msg=productlinks_edit_not_found
				return HttpResponseRedirect('/crud/productlinks/?msg=%s' % (msg))


			reqpost = request.POST.copy()
			if len(reqpost['linkdescription']) < 3:
				reqpost['linkdescription'] = p.linkdescription

			formset = ProductLinksFormAll(reqpost, instance=p)
			if formset.is_valid():
				formset.save()
				msg=productlinks_edit_ok
				return HttpResponseRedirect('/crud/productlinks/?notify=%s' % (msg))

			else:
				msg = productlinks_edit_not_found
				return HttpResponseRedirect('/crud/productlinks/?msg=%s' % (msg))



@login_required
def parent_categories(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(CategoryParent.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(CategoryParent.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])

		return render_to_response('crud/parent_categories.html', {
				
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_parent_categories(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_parent_categories.html', {
			
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_parent_categories_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = CategoryParentForm(request.POST, request.FILES)
			new_f = f.save()
			msg = parent_categories_added
			return HttpResponseRedirect('/crud/parent_categories/?notify=%s' % (msg))
		except ValueError:
			msg = parent_categories_error
			return HttpResponseRedirect('/crud/parent_categories/?msg=%s' % (msg))



@login_required
def edit_parent_categories(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				p = CategoryParent.objects.get(pk=int(id))
			except:
				msg=parent_categories_edit_not_found
				return HttpResponseRedirect('/crud/parent_categories/?msg=%s' % (msg))

			gets = get_get(request)
			f = CategoryParentForm(instance=p)
			return render_to_response('crud/edit_parent_categories.html', {
				'p':p,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				p = CategoryParent.objects.get(pk=int(id))
			except:
				msg=parent_categories_edit_not_found
				return HttpResponseRedirect('/crud/parent_categories/?msg=%s' % (msg))
			formset = CategoryParentForm(request.POST, instance=p)
			if formset.is_valid():
				formset.save()
				msg=parent_categories_edit_ok
				return HttpResponseRedirect('/crud/parent_categories/?notify=%s' % (msg))

			else:
				msg = parent_categories_edit_not_found
				return HttpResponseRedirect('/crud/parent_categories/?msg=%s' % (msg))






@login_required
def product_link_profiles(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)


		linksprofiles = LinksProfile.objects.all()
		linkprofile_dict = []
		for i in linksprofiles:
			linkprofile_dict.append({
				'obj':i,
				'imagelinks':len(i.imagelinks.all()),
				'bannerlinks':len(i.bannerlinks.all()),
				'txtlinks':len(i.textlinks.all()),
				'productlinks':len(i.products.all()),
			})
		#


		if gets['orderby'] == 'n':
			paginator = Paginator(linkprofile_dict, C_SETTING.paginate_count)
		else:
			paginator = Paginator(linkprofile_dict, C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])

		return render_to_response('crud/product_link_profiles.html', {
				
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_product_link_profiles(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_product_link_profiles.html', {
			
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_product_link_profiles_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = LinksProfileForm(request.POST, request.FILES)
			new_f = f.save()
			msg = product_link_profiles_added
			return HttpResponseRedirect('/crud/product_link_profiles/?notify=%s' % (msg))
		except ValueError:
			msg = product_link_profiles_error
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=%s' % (msg))



def edit_product_link_profiles(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				p = LinksProfile.objects.get(pk=int(id))
			except:
				msg=product_link_profiles_edit_not_found
				return HttpResponseRedirect('/crud/product_link_profiles/?msg=%s' % (msg))

			gets = get_get(request)
			f = LinksProfileForm(instance=p)
			return render_to_response('crud/edit_product_link_profiles.html', {
				'p':p,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				p = LinksProfile.objects.get(pk=int(id))
			except:
				msg=product_link_profiles_edit_not_found
				return HttpResponseRedirect('/crud/product_link_profiles/?msg=%s' % (msg))

			formset = LinksProfileForm(request.POST, instance=p)

			if formset.is_valid():
				formset.save()
				msg=product_link_profiles_edit_ok
				return HttpResponseRedirect('/crud/product_link_profiles/?notify=%s' % (msg))

			else:
				msg = product_link_profiles_edit_not_found
				return HttpResponseRedirect('/crud/product_link_profiles/?msg=%s' % (msg))


@login_required
def linkprofile_selection(request, id):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		try:
			profile=LinksProfile.objects.get(pk=int(id))
		except:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=NoProfileID')

		if gets['orderby'] == 'n':
			paginator = Paginator(ProductLinks.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(ProductLinks.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])
		linkdict = []

		for i in p.object_list:
			usedin = 'n'
			in_products = 'n'
			in_image = 'n'
			in_banner = 'n'
			in_txt = 'n'
			if i in profile.products.all():
				in_products = 'y'
				usedin = 'y'
			if i in profile.textlinks.all():
				in_txt = 'y'
				usedin = 'y'
			if i in profile.imagelinks.all():
				in_img = 'y'
				usedin = 'y'
			if i in profile.bannerlinks.all():
				in_banner = 'y'
				usedin = 'y'


			linkdict.append(
					{'obj':i,
					'usedin':usedin,
					'in_products':in_products,
					'in_banner':in_banner,
					'in_image':in_image,
					'in_txt':in_txt,
					}
			)
		

		return render_to_response('crud/linkprofileselection.html', {
				'sitepages':SitePages.objects.all(),
						'websites':Websites.objects.all(),
			
						'profile':profile,
						'products':linkdict,

						
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)


@login_required
def linkprofile_addlink(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		try:
			productid = request.GET.get('pid','n')
		except ValueError:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=System:NoPID')
		try:
			lpid = int(request.GET.get('lpid',0))
		except ValueError:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=System:NoLPID')
		try:
			l=LinksProfile.objects.get(pk=lpid)
			p=ProductLinks.objects.get(pk=int(productid))
		except:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=System:CouldNotGetObjects')
		if p.linktype == 'txt':
			l.textlinks.add(p)
		if p.linktype == 'img':
			l.imagelinks.add(p)
		if p.linktype == 'banner':
			l.bannerlinks.add(p)
		if p.linktype == 'product':
			l.products.add(p)

		return render_to_response('crud/windowclose.html',{})

@login_required
def linkprofile_dellink(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		try:
			productid = request.GET.get('pid','n')
		except ValueError:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=System:NoPID')
		try:
			lpid = int(request.GET.get('lpid',0))
		except ValueError:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=System:NoLPID')
		try:
			l=LinksProfile.objects.get(pk=int(lpid))
			p=ProductLinks.objects.get(pk=int(productid))
		except:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=System:CouldNotGetObjects')
		if p.linktype == 'txt':
			l.textlinks.remove(p)
		if p.linktype == 'img':
			l.imagelinks.remove(p)
		if p.linktype == 'banner':
			l.bannerlinks.remove(p)
		if p.linktype == 'product':
			l.products.remove(p)

		return render_to_response('crud/windowclose.html',{})

@login_required()
def sitepage_products_bulk(request):
	if request.user.is_staff == 1:
		if request.method == 'POST':
			profileid = request.POST['profileid']
			checkbox_list = request.POST.getlist('prod')
			for productid in checkbox_list:
				if str(request.POST['action']) == 'add':
					l=LinksProfile.objects.get(pk=int(profileid))
					p = ProductLinks.objects.get(pk=int(productid))

					if p.linktype == 'txt':
						l.textlinks.add(p)
						l.save()
					if p.linktype == 'img':
						l.imagelinks.add(p)
						l.save()
					if p.linktype == 'banner':
						l.bannerlinks.add(p)
						l.save()
					if p.linktype == 'product':
						l.products.add(p)
						l.save()



				if str(request.POST['action']) == 'delete':
					l=LinksProfile.objects.get(pk=int(profileid))
					p = ProductLinks.objects.get(pk=int(productid))

					if p.linktype == 'txt':
						l.textlinks.remove(p)
						l.save()
					if p.linktype == 'img':
						l.imagelinks.remove(p)
						l.save()
					if p.linktype == 'banner':
						l.bannerlinks.remove(p)
						l.save()
					if p.linktype == 'product':
						l.products.remove(p)
						l.save()

			return render_to_response('crud/windowclose.html',{})




# -- content 
@login_required
def content_article_categories(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(ContentCategory.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(ContentCategory.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])

		return render_to_response('crud/content_article_categories.html', {
				
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_content_article_categories(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_content_article_categories.html', {
				'categoryparent':CategoryParent.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_content_article_categories_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = ContentCategoryForm(request.POST, request.FILES)
			new_f = f.save()
			msg = content_article_categories_added
			return HttpResponseRedirect('/crud/content_article_categories/?notify=%s' % (msg))
		except ValueError:
			msg = content_article_categories_error
			return HttpResponseRedirect('/crud/content_article_categories/?msg=%s' % (msg))



@login_required
def edit_content_article_categories(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				p = ContentCategory.objects.get(pk=int(id))
			except:
				msg=content_article_categories_edit_not_found
				return HttpResponseRedirect('/crud/content_article_categories/?msg=%s' % (msg))

			gets = get_get(request)
			f = ContentCategoryForm(instance=p)
			return render_to_response('crud/edit_content_article_categories.html', {
				'p':p,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				p = ContentCategory.objects.get(pk=int(id))
			except:
				msg=content_article_categories_edit_not_found
				return HttpResponseRedirect('/crud/content_article_categories/?msg=%s' % (msg))
			formset = ContentCategoryForm(request.POST, instance=p)
			if formset.is_valid():
				formset.save()
				msg=content_article_categories_edit_ok
				return HttpResponseRedirect('/crud/content_article_categories/?notify=%s' % (msg))

			else:
				msg = content_article_categories_edit_not_found
				return HttpResponseRedirect('/crud/content_article_categories/?msg=%s' % (msg))


@login_required
def content_articles(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		if gets['orderby'] == 'n':
			paginator = Paginator(ContentArticles.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(ContentArticles.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])

		return render_to_response('crud/content_articles.html', {
				
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_content_articles(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_content_articles.html', {
				'contentcategory':ContentCategory.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)


@login_required()
def new_content_articles_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = ContentArticlesFormAll(request.POST)
			try:
				new_f = f.save()
				msg = content_articles_added

				return HttpResponseRedirect('/crud/content_articles/?notify=%s' % (msg))
			except:
				msg = content_articles_error
				return HttpResponseRedirect('/crud/content_articles/?msg=%s' % (msg))

		except ValueError:
			msg = content_articles_error
			return HttpResponseRedirect('/crud/content_articles/?msg=%s' % (msg))



@login_required
def edit_content_articles(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				p = ContentArticles.objects.get(pk=int(id))
			except:
				msg=content_articles_edit_not_found
				return HttpResponseRedirect('/crud/content_articles/?msg=%s' % (msg))

			gets = get_get(request)
			f = ContentArticlesForm(instance=p)
			return render_to_response('crud/edit_content_articles.html', {
				'p':p,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				p = ContentArticles.objects.get(pk=int(id))
			except:
				msg=content_articles_edit_not_found
				return HttpResponseRedirect('/crud/content_articles/?msg=%s' % (msg))

			reqpost = request.POST.copy()
			if len(reqpost['body']) < 3:
				reqpost['body'] = p.body


			formset = ContentArticlesFormAll(reqpost, instance=p)
			if formset.is_valid():
				formset.save()
				msg=content_articles_edit_ok
				return HttpResponseRedirect('/crud/content_articles/?notify=%s' % (msg))

			else:
				msg = content_articles_edit_not_found
				return HttpResponseRedirect('/crud/content_articles/?msg=%s' % (msg))







@login_required
def content_profiles(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)


		contentprofiles = ContentProfile.objects.all()
		contentprofiles_dict = []
		for i in contentprofiles:
			contentprofiles_dict.append({
				'obj':i,
				'articles':len(i.articles.all()),
				
			})
		#


		if gets['orderby'] == 'n':
			paginator = Paginator(contentprofiles_dict, C_SETTING.paginate_count)
		else:
			paginator = Paginator(contentprofiles_dict, C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])

		return render_to_response('crud/content_profiles.html', {
				
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)

@login_required
def new_content_profiles(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)
		return render_to_response('crud/new_content_profiles.html', {
				'articles':ContentArticles.objects.all(),
				'msg':gets['msg'],'notify':gets['notify'],
				
			}
		)

		# FINISH THESE NEW AND EDIT .. TOO TIRED

@login_required()
def new_content_profiles_post(request):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		try:
			f = ContentProfileForm(request.POST, request.FILES)
			new_f = f.save()
			msg = content_profiles_added
			if str(request.POST['addarticles']) == 'y':
				return HttpResponseRedirect('/crud/contentprofile_selection/%s' % (new_f.id))
			else:
				return HttpResponseRedirect('/crud/content_profiles/?notify=%s' % (msg))
		except ValueError:
			msg = content_profiles_error
			return HttpResponseRedirect('/crud/content_profiles/?msg=%s' % (msg))



def edit_content_profiles(request, id):
	if not request.user.is_staff == 1:
		return HttpResponseRedirect('/login')
	else:
		if not request.method == 'POST':
			try:
				p = ContentProfile.objects.get(pk=int(id))
			except:
				msg=content_profiles_edit_not_found
				return HttpResponseRedirect('/crud/content_profiles/?msg=%s' % (msg))

			gets = get_get(request)
			f = ContentProfileForm(instance=p)
			return render_to_response('crud/edit_content_profiles.html', {
				'p':p,
				'form':f,'msg':gets['msg'],'notify':gets['notify'],
			})

		if request.method == 'POST':
			# change this duh
			try:
				p = ContentProfile.objects.get(pk=int(id))
			except:
				msg=content_profiles_edit_not_found
				return HttpResponseRedirect('/crud/content_profiles/?msg=%s' % (msg))

			formset = ContentProfileFormAll(request.POST, instance=p)

			if formset.is_valid():
				formset.save()
				msg=content_profiles_edit_ok
				return HttpResponseRedirect('/crud/content_profiles/?notify=%s' % (msg))

			else:
				msg = content_profiles_edit_not_found
				return HttpResponseRedirect('/crud/content_profiles/?msg=%s' % (msg))



@login_required
def contentprofile_selection(request, id):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		gets = get_get(request)

		try:
			profile=ContentProfile.objects.get(pk=int(id))
		except:
			return HttpResponseRedirect('/crud/product_link_profiles/?msg=NoProfileID')

		if gets['orderby'] == 'n':
			paginator = Paginator(ContentArticles.objects.all(), C_SETTING.paginate_count)
		else:
			paginator = Paginator(ContentArticles.objects.all().order_by(gets['orderby']), C_SETTING.paginate_count)

		try:
			p = paginator.page(gets['page'])
		except (EmptyPage, InvalidPage):
			p = paginator.page(paginator.num_pages)

		page_urls = paginate_urls(p, gets['orderby'])
		linkdict = []

		for i in p.object_list:
			usedin = 'n'
				

			if i in profile.articles.all():
				in_products = 'y'
				usedin = 'y'
				


			linkdict.append(
					{'obj':i,
					'usedin':usedin,
					}
			)
		

		return render_to_response('crud/contentprofile_selection.html', {
				'sitepages':SitePages.objects.all(),
						'websites':Websites.objects.all(),
			
						'profile':profile,
						'articles':linkdict,

						
				'page':gets['page'],'p':p,
				'nexturl':page_urls['nexturl'],'prevurl':page_urls['prevurl'],
				'msg':gets['msg'],'notify':gets['notify'],
			}
		)


@login_required
def contentprofile_addlink(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		try:
			contentid = request.GET.get('pid','n')
		except ValueError:
			return HttpResponseRedirect('/crud/content_profiles/?msg=System:NoPID')
		try:
			cpid = int(request.GET.get('cpid',0))
		except ValueError:
			return HttpResponseRedirect('/crud/content_profiles/?msg=System:NoLPID')
		try:
			l=ContentProfile.objects.get(pk=cpid)
			p=ContentArticles.objects.get(pk=int(contentid))
		except:
			return HttpResponseRedirect('/crud/content_profiles/?msg=System:CouldNotGetObjects')

		l.articles.add(p)

		return render_to_response('crud/windowclose.html',{})



@login_required
def contentprofile_dellink(request):
	if not request.user.is_staff == 1:

		return HttpResponseRedirect('/login')
	else:
		try:
			contentid = request.GET.get('pid','n')
		except ValueError:
			return HttpResponseRedirect('/crud/content_profiles/?msg=System:NoPID')
		try:
			cpid = int(request.GET.get('cpid',0))
		except ValueError:
			return HttpResponseRedirect('/crud/content_profiles/?msg=System:NoLPID')
		try:
			l=ContentProfile.objects.get(pk=int(cpid))
			p=ContentArticles.objects.get(pk=int(contentid))
		except:
			return HttpResponseRedirect('/crud/content_profiles/?msg=System:CouldNotGetObjects')
	
		l.articles.remove(p)

		return render_to_response('crud/windowclose.html',{})




@login_required()
def contentprofile_bulk(request):
	if request.user.is_staff == 1:
		if request.method == 'POST':
			profileid = request.POST['profileid']
			checkbox_list = request.POST.getlist('prod')
			for productid in checkbox_list:
				if str(request.POST['action']) == 'add':
					l=ContentProfile.objects.get(pk=int(profileid))
					p = ContentArticles.objects.get(pk=int(productid))

					
					l.articles.add(p)
					l.save()



				if str(request.POST['action']) == 'delete':
					l=ContentProfile.objects.get(pk=int(profileid))
					p = ContentArticles.objects.get(pk=int(productid))

					
					l.articles.remove(p)
					l.save()

			return render_to_response('crud/windowclose.html',{})


	else:
		return HttpResponseRedirect('/crud/content_profiles')






@login_required()
def edit_settings(request):
	if request.user.is_staff == 1:
		if request.method == 'POST':
			c_settings_data = """
product_categories_name_url='%s'
product_name_url='%s'
content_categories_name_url='%s'
content_name_url='%s'
show_bug='%s'
product_per_page_count='%s'
imagelink_per_page_count='%s'
textlink_per_page_count='%s'
paginate_count=%s
			""" % (
				request.POST['product_categories_name_url'],
				request.POST['product_name_url'],
				request.POST['content_categories_name_url'],
				request.POST['content_name_url'],
				request.POST['show_bug'],
				request.POST['product_per_page_count'],
				request.POST['imagelink_per_page_count'],
				request.POST['textlink_per_page_count'],
				request.POST['paginate_count'],
			)
			dir_root = SETTING.CUSTOM_SITEROOT
			dat = []
			o = open('%scrud/CustomSettings.py'%(dir_root), 'w')
			o.write(c_settings_data)
			o.close()
			return HttpResponseRedirect('/crud/edit_settings/')

		else:
			csetting = {	
				'product_categories_name_url':C_SETTING.product_categories_name_url,
				'product_name_url':C_SETTING.product_name_url,
				'content_categories_name_url':C_SETTING.content_categories_name_url,
				'content_name_url':C_SETTING.content_name_url,
				'show_bug':C_SETTING.show_bug,
				'product_per_page_count':C_SETTING.product_per_page_count,
				'imagelink_per_page_count':C_SETTING.imagelink_per_page_count,
				'textlink_per_page_count':C_SETTING.textlink_per_page_count,
				'paginate_count':C_SETTING.paginate_count,
			}
		
		
			return render_to_response('crud/edit_settings.html',{'setting':csetting})


