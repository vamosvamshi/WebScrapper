from django import forms

class FormName_amazon(forms.Form):
    AmazonProductCode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E.g. B01LYHL9YY'}),label='Amazon ASIN Code')

class FormName_bestbuy(forms.Form):
    BestBuyProductCode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E.g. 5835851'}),label='BestBuy Product ID')

class FormName_ebay(forms.Form):
    EbayProductCode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E.g. 110891711'}),label='Ebay Item No.')

class FormName_google(forms.Form):
    GoogleCompanyTicker = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E.g. MSFT,GE'}),label='Google Finance Company Code')
    StartDay = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 31'}),label='Start Day')
    StartMonth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 12'}),label='Start Month')
    StartYear = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'from 1970 to present'}),label='Start Year')
    EndDay = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 31'}),label='End Day')
    EndMonth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 12'}),label='End Month')
    EndYear = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'from 1970 to present'}),label='End Year')

    def clean(self):
        all_clean_data = super().clean()
        StartDay = all_clean_data['StartDay']
        StartMonth = all_clean_data['StartMonth']
        StartYear = all_clean_data['StartYear']
        EndDay = all_clean_data['EndDay']
        EndMonth = all_clean_data['EndMonth']
        EndYear = all_clean_data['EndYear']

        if int(StartDay)<1 or int(StartDay)>31:
            raise forms.ValidationError("MAKE SURE START DATE IS A VALID ONE")
        if int(StartMonth)<1 or int(StartMonth)>12:
            raise forms.ValidationError("MAKE SURE START MONTH IS A VALID ONE")
        if int(EndDay)<1 or int(EndDay)>31:
            raise forms.ValidationError("MAKE SURE END MONTH IS A VALID ONE")
        if int(EndMonth)<1 or int(EndMonth)>12:
            raise forms.ValidationError("MAKE SURE END YEAR IS A VALID ONE")
        if int(StartYear)>=int(EndYear):
            raise forms.ValidationError("START YEAR AND END YEAR HAS TO BE DIFFERENT")

class FormName_yahoo(forms.Form):
    YahooCompanyTicker = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'E.g. MSFT,GE'}),label='Yahoo Finance Company Code')
    StartDay = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 31'}),label='Start Day')
    StartMonth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 12'}),label='Start Month')
    StartYear = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'from 1970 to present'}),label='Start Year')
    EndDay = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 31'}),label='End Day')
    EndMonth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'1 - 12'}),label='End Month')
    EndYear = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'from 1970 to present'}),label='End Year')

    def clean(self):
        all_clean_data = super().clean()
        StartDay = all_clean_data['StartDay']
        StartMonth = all_clean_data['StartMonth']
        StartYear = all_clean_data['StartYear']
        EndDay = all_clean_data['EndDay']
        EndMonth = all_clean_data['EndMonth']
        EndYear = all_clean_data['EndYear']

        if int(StartDay)<1 or int(StartDay)>31:
            raise forms.ValidationError("MAKE SURE START DATE IS A VALID ONE")
        if int(StartMonth)<1 or int(StartMonth)>12:
            raise forms.ValidationError("MAKE SURE START MONTH IS A VALID ONE")
        if int(EndDay)<1 or int(EndDay)>31:
            raise forms.ValidationError("MAKE SURE END MONTH IS A VALID ONE")
        if int(EndMonth)<1 or int(EndMonth)>12:
            raise forms.ValidationError("MAKE SURE END YEAR IS A VALID ONE")
        if int(StartYear)>=int(EndYear):
            print ("start year "+StartYear+" end year "+EndYear)
            raise forms.ValidationError("START YEAR AND END YEAR HAS TO BE DIFFERENT")
