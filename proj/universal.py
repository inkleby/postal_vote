from django.conf import settings # import the settings file



def universal_context(request):
    """
    returns helpful universal context to the views
    """

    
    return {'IS_LIVE': settings.IS_LIVE,
            'GA_CODE':settings.GA_CODE,
            'request':request,
            'current_path': settings.SITE_ROOT + request.get_full_path(),
            'main_menu':settings.MAIN_MENU,
            'site_name':settings.SITE_NAME,
            'share_image':settings.SHARE_IMAGE,
            'site_desc':settings.SITE_DESC,
            'twitter_handle':settings.SITE_TWITTER}