@permission_required('core.agent_perm')
def lead_list(request, admin=False):
   """ My leads and admin leads page, depending on admin flag.  My leads is filtered to that agent's assigned leads. """

   filters = {}
   form = {}
   or_filter = sort = None

   if admin:
       if not request.user.has_perm('core.office_manager_perm') and not request.user.has_perm('core.manager_perm'):
           return HttpResponseForbidden
       access_filter = Q()
   else:
       try:
           team = request.user.profile.team
       except AttributeError:
           team = None

       if team:
           if team.shared_leads:
               access_filter = Q(assigned_agent=request.user) | Q(assigned_agent__profile__team=team)
           else:
               access_filter = Q(assigned_agent=request.user)
       else:
           access_filter = Q(assigned_agent=request.user)

   leads = Lead.objects.all()

   if request.method == 'GET':
       # create a form instance and populate it with data from the request:
       form = LeadSearchForm(request.GET, request_user=request.user) if not admin else LeadSearchAdminForm(request.GET)

       # check whether it's valid:
       if form.is_valid():
           # process the data in form.cleaned_data as required
           search = form.cleaned_data['search']
           status = form.cleaned_data['status']
           lead_type = form.cleaned_data['lead_type']
           assigned_agent = form.cleaned_data.get('assigned_agent')
           unassigned = form.cleaned_data.get('unassigned')
           stage = form.cleaned_data['stage']
           lead_source = form.cleaned_data['lead_source']
           created_after = form.cleaned_data['created_after']
           created_before = form.cleaned_data['created_before']
           score = form.cleaned_data['score']
           sort = form.cleaned_data['sort']

           if lead_type:
               filters['lead_type__in'] = lead_type

           if status:
               filters['status__in'] = status

           if search:
               search_split = search.split()
               cleaned_number = clean_number(search)
               cleaned_number = cleaned_number if (len(cleaned_number) > 2) else '#####'
               or_filter = Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(phone_index__contains=cleaned_number) | Q(spouse_name__icontains=search)

               if len(search_split) > 1:
                   for term in search_split:
                       print(term)
                       or_filter = or_filter | Q(first_name__icontains=term) | Q(last_name__icontains=term)

               leads = leads.filter(or_filter)

           if assigned_agent:
               filters['assigned_agent'] = assigned_agent

           if unassigned is not None:
               filters['assigned_agent__isnull'] = unassigned

           if stage:
               filters['stage'] = stage

           if lead_source:
               filters['lead_source'] = lead_source

           if created_after:
               filters['lead_time__date__gte'] = created_after

           if created_before:
               filters['lead_time__date__lte'] = created_before

           if score:
               filters['lead_score__gte'] = score
   else:
       return HttpResponseNotAllowed(['GET'])

   reminder_prefetch = Prefetch(
       "lead_reminders",
       queryset=Reminder.objects.all().order_by('reminder_time'),
   )

   if sort:
       if sort == 'inquiry':
           sort_order = ['-last_inquiry', '-last_active']
       if sort == 'activity':
           sort_order = ['-last_active']
       elif sort == 'update':
           sort_order = ['-date_edited']
       elif sort == 'score':
           sort_order = ['-lead_score']
       elif sort == 'call':
           sort_order = ['last_contact_phone']
   else:
       sort_order = ['-last_comm']

   leads = leads.filter(**filters).filter(access_filter).order_by(*sort_order).prefetch_related(reminder_prefetch)[:3000]

   page = request.GET.get('p')
   paginator = Paginator(leads, 50)  # Show 50 items per page

   try:
       lead_list = paginator.page(page)
   except PageNotAnInteger:
       # If page is not an integer, deliver first page.
       lead_list = paginator.page(1)
   except EmptyPage:
       # If page is out of range (e.g. 9999), deliver last page of results.
       lead_list = paginator.page(paginator.num_pages)

   num_results = leads.count()
   lead_source_options = get_lead_source_options()

   return render(request, "leads/lead_list.html", {'leads': lead_list, 'form': form, 'num_results': num_results, 'admin': admin, 'lead_source_options': lead_source_options})
