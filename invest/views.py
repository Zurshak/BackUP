import requests
from bs4 import BeautifulSoup
from django.shortcuts import render , HttpResponse
from .models import Paper
from .forms import PaperForm
from django.db.models import Count, Sum, Avg

def index(request):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
	def getFin(symbol):
		url = r'https://finviz.com/quote.ashx?t={}'.format(symbol.lower())
		response = requests.get(url, headers=headers).text
		soup = BeautifulSoup(response, 'html.parser')
		pb = soup.find(text="Price")
		pb = pb.find_next(class_='snapshot-td2').text
		return float(pb)


	usd_url = 'https://www.sravni.ru/bank/tinkoff-bank/valjuty/'


	usd_res = requests.get(usd_url)
	usd_soup = BeautifulSoup(usd_res.content, 'html.parser')
	usd_now = float(usd_soup.findAll("td", {"class": "table-light__cell bold bold--mobile-normal"})[0].text[0:5].replace(',', '.'))



	papers = Paper.objects.all()
	allpapers = []
	agg_row = Paper.objects.all().aggregate(tot=Count('dollar_price'))
	row_numb = int(agg_row['tot'])
	agg_avg_old_dollar = Paper.objects.all().aggregate(tot=Avg('dollar_price'))
	avg_dollar = round(float(agg_avg_old_dollar['tot']), 2)


	if(request.method == "POST"):
		form = PaperForm(request.POST)
		form.save()

	form = PaperForm()


	for paper in papers:
		now_price = getFin(paper.name)

		paperinfo = {
			'paper': paper.name,
			'nn': paper.nn,
			'paper_price': paper.paper_price,
			'stack_price': round(paper.paper_price*paper.nn ,2),
			'broker_pay': paper.broker_pay,
			'total_pay': round((paper.paper_price*paper.nn)+paper.broker_pay ,2),
			'dollar_price': paper.dollar_price,
			'rub_pay': round(paper.dollar_price*((paper.paper_price*paper.nn)+paper.broker_pay),2),
			'now_price': now_price,
			'usd_now': usd_now,
			'usd_growth': round((now_price*paper.nn)-(((paper.paper_price*paper.nn)+paper.broker_pay)) , 2),
			'rub_growth': round((now_price*usd_now*paper.nn)-(((paper.paper_price*paper.dollar_price*paper.nn) + paper.dollar_price*paper.broker_pay)), 2),
			'dollar_growth': round(100 - ((paper.paper_price + paper.broker_pay) / (now_price) * 100), 2),
			'pyb_growth': round(100 - ((paper.paper_price*paper.dollar_price + paper.broker_pay*paper.dollar_price) / (now_price*usd_now) * 100), 2),
		}

		allpapers.append(paperinfo)


	context_from_magic = {'all_info':allpapers}

	StackTotal = 0.00
	i = 0
	while i < row_numb:
		StackTotal = StackTotal + context_from_magic['all_info'][i]['stack_price']
		i = i + 1
		stack_total = round(StackTotal,2)

	BrokerTotal = 0.00
	i = 0
	while i < row_numb:
		BrokerTotal = BrokerTotal + context_from_magic['all_info'][i]['broker_pay']
		i = i + 1
		broker_total=round(BrokerTotal,2)

	EndTotal = 0.00
	i = 0
	while i < row_numb:
		EndTotal = EndTotal + context_from_magic['all_info'][i]['total_pay']
		i = i + 1
		end_total = round(EndTotal,2)

	RubTotal = 0.00
	i = 0
	while i < row_numb:
		RubTotal = RubTotal + float(context_from_magic['all_info'][i]['rub_pay'])
		i = i + 1
		rub_total = round(RubTotal, 2)

	USDTotal=0.00
	i=0
	while i < row_numb:
		USDTotal = USDTotal + float(context_from_magic['all_info'][i]['usd_growth'])
		i = i+1
		usd_tot_growh = round(USDTotal,2)

	RUBTotal = 0.00
	i = 0
	while i < row_numb:
		RUBTotal = RUBTotal + float(context_from_magic['all_info'][i]['rub_growth'])
		i = i + 1
		rub_tot_growth = round(RUBTotal, 2)

		total_usd_prsnt = round(100 - ((end_total / (end_total + usd_tot_growh) * 100)),2)
		total_rub_prsnt = round(100 - ((rub_total / (rub_total + rub_tot_growth) * 100)),2)


		context = {'all_info': allpapers, 'form': form,
				   'end_total': end_total, 'broker_total':broker_total, 'stack_total':stack_total, 'avg_dollar': avg_dollar,'rub_total':rub_total,
				   'usd_tot_growh':usd_tot_growh,'rub_tot_growth':rub_tot_growth,'total_usd_prsnt':total_usd_prsnt,'total_rub_prsnt':total_rub_prsnt}


		#return HttpResponse(usd_parse)

	return render(request, 'invest/index.html', context)