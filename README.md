PURPOSE:

1. On the base of particular strategy/ calculation, the app assigns weights to set of companies and buys/ sells them accordingly.
	Makes simulation and see wether it performs better than a simple investing in the same instruments over period of time 
  (like buying and holding long-term).
  

DEVELOPMENT NOTES (to be ordered if the project is to be continued):

How does Python Stock App works at the moment:

1. Split the whole period into sub-periods.
2. For each sub-period:
	1. Get weights.
		1. For each company:
			1. Get EPS, get share price, return EPS/ share price
    2. Calculate income using weights.
3. Return whole-period income, and the real change in this whole period.


Flaws and Limitations:

1. It may not be accurate as if the “action” day is weekend, then closing of previous period and start of the next one will be two different days. It causes difference between just ‘average change’ in this period.
2. Is taking ‘close’ price a good choice for the action? In practice I couldn’t sell/ buy when the close price is known (after the market closing).
3. FCF:
    1. amount of shares -> best would be to use amountOfShares from the same day as the stock price comes from. Worse would be the financialQuarter day amountOfShares, and the worst - “today” (day of fetching from API)
    2. For now we can use the report day commonStock or weightedAverageShsOut
4. Known issues - Cosmetics:	
    1. Unused numberOfPeriods in getMostRecentIncomeStatementForGivenCompanyForGivenDate_nPeriods in DatabaseUtils
5. Known issues - Logic:
	1. Question about correctness of weightedAverageShsOut usage.
	2. I’m currently using only FCF instead of the whole InstrinsicValue
	3. I take 4 last months into account to get average. Maybe I should get only 1 actually?
		It is showing how the company performs in longer term, but also doesn’t reflect changes correctly (they’re minimised).


Python Stock App - MAIN PLAN

1. What I would like to test:
	I would like to test whether the values of IntrinsicValue per 1 spent today dollar are fluctuating over time and crossing each other on the graph.
	If so, it means I can make money by betting on the underpriced and against overpriced.
	Otherwise it would mean that the stock price doesn’t depend on the IntrinsicValue (per 1 dollar spent).

	I should get Intrinsic Value of the company on the given day (using recent financial reports).
	I should get Amount of Shares of the company on the given day.
	I should get Share Price of the company on the given day.
	I should calculate the value = Intrinsic Value / Amount of Shares / Share Price

2. What I am actually testing:
	I get the average FCF from the last 4 quarter financial reports.
	I get the weightedAverageShsOut from the last report as the Amount of Shares.
		Maybe commonShares would be better?
	I get the Share Price of the company on the given day.

	What about the date? Is fillingDate a correct date?
		We use it when fetching a correct Income Statement.
		So I have some date, and I wanna fetch closest past income statements for this date.
		Filling date seems to be okay as according to stackexchange.com it's the date when the report is published.


The Stock App 4 - Improvements

1. Add comparison of values/ spent dollar with previous months
    1. We need to take into account that between the date month ago and today - there could be a quarter results release day.
    2. So if there was this day in between - then take the ‘previous one’ into account. Else - recent one.
    3. Then fetch stock price on that date.
    4. Then fetch amount of outsanding shares on that day.
        1. DIFFICULT
    5. If I could get stock price day by day (easy), and oustanding shares day by day (more difficult), and previous income statement data (net income) (moderate), I could make a proper simulation in Google Sheets.

2. Simplified version of the comparison:
    1. Get the stock price 30 days ago.
    2. Use current oustanding_shares value
    3. Use ‘recent’ net income/ gross profit value.

3. Fix why some companies cannot be added:
    1. ABEPF
    2. DAI
    3. OCDO

Next Steps:

1. Negative values!
2. Older Data - up to 2008 or 2000 crisis?
