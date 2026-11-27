# make_planner.py — builds "Paycheck Planner.xlsx", the product sold from the channel. python3 make_planner.py
import datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as CL
from openpyxl.comments import Comment

wb = Workbook()
NAVY, GREEN = "0C1A2A", "1F9D6B"
F = lambda **k: Font(name="Arial", **k)
INP = dict(font=F(color="0000FF", size=11), fill=PatternFill("solid", fgColor="FFF59D"))
HEAD = dict(font=F(bold=True, color="FFFFFF"), fill=PatternFill("solid", fgColor=NAVY))
thin = Border(bottom=Side(style="thin", color="C9D2DC"))
USD, USD2 = '$#,##0;($#,##0);"-"', '$#,##0.00;($#,##0.00);"-"'

def style(c, **k):
    for a, v in k.items(): setattr(c, a, v)
def title(ws, text, sub):
    ws["A1"] = text; ws["A1"].font = F(bold=True, size=18, color=NAVY)
    ws["A2"] = sub; ws["A2"].font = F(size=10, color="6B7A8C", italic=True)
def inp(c, v, fmt=None):
    c.value = v; style(c, **INP)
    if fmt: c.number_format = fmt
def head(ws, row, cols):
    for i, h in enumerate(cols):
        c = ws.cell(row, i + 1, h); style(c, **HEAD); c.alignment = Alignment(horizontal="center", wrap_text=True)
def widths(ws, ws_):
    for i, w in enumerate(ws_): ws.column_dimensions[CL(i + 1)].width = w
def fontall(ws):
    for row in ws.iter_rows():
        for c in row:
            if c.font and c.font.name != "Arial": c.font = F(bold=c.font.b, italic=c.font.i, color=c.font.color, size=c.font.sz)

# ------------------------------------------------------------- Start Here
st = wb.active; st.title = "Start Here"
pp = wb.create_sheet("Paycheck Plan"); sf = wb.create_sheet("Surprise Fund"); dp = wb.create_sheet("Debt Payoff"); sc = wb.create_sheet("Payoff Schedule")

# ------------------------------------------------------------- Paycheck Plan
title(pp, "Paycheck Plan", "Give every bill a paycheck, even them out, then give the leftovers one job.")
inputs = [("Take-home pay per paycheck", 1850, USD), ("Paycheck 2 arrives around day", 15, "0"),
          ("Buffer moved from paycheck 2 to paycheck 1", 400, USD), ("Groceries & gas, per paycheck", 320, USD), ("Fun money, per paycheck", 100, USD)]
for i, (lab, v, fmt) in enumerate(inputs):
    pp.cell(3 + i, 1, lab).font = F(); inp(pp.cell(3 + i, 2), v, fmt)
pp["C5"] = '="Suggested: "&TEXT(ROUND((H6-G6)/2,-1),"$#,##0")'; pp["C5"].font = F(size=9, color="6B7A8C", italic=True)
pp["B4"].comment = Comment("Bills due before this day are paid from paycheck 1; bills due on or after it, from paycheck 2.", "Paycheck Math")
head(pp, 11, ["Bill", "Amount", "Due day (1-31)", "Paid from paycheck"])
bills = [("Rent", 1300, 1), ("Phone", 65, 8), ("Student loan", 220, 10), ("Car payment", 340, 15), ("Internet", 60, 20),
         ("Insurance", 140, 22), ("Utilities", 150, 25), ("Credit card minimum", 96, 28)]
for r in range(12, 37):
    b = bills[r - 12] if r - 12 < len(bills) else ("", None, None)
    inp(pp.cell(r, 1), b[0] or None); inp(pp.cell(r, 2), b[1], USD); inp(pp.cell(r, 3), b[2], "0")
    pp.cell(r, 4, f'=IF(OR(A{r}="",C{r}=""),"",IF(C{r}<$B$4,1,2))').alignment = Alignment(horizontal="center")
pp["A37"] = "Example rows show the numbers from the video. Type over them with your own bills (up to 25)."; pp["A37"].font = F(size=9, italic=True, color="6B7A8C")
head(pp, 3, []); 
for c, h in zip("FGH", ["Per paycheck", "Paycheck 1", "Paycheck 2"]):
    style(pp[f"{c}3"], **HEAD); pp[f"{c}3"].value = h
rows = [("Take-home pay", "=$B$3", "=$B$3"),
        ("Bills", "=SUMIFS($B$12:$B$36,$D$12:$D$36,1)", "=SUMIFS($B$12:$B$36,$D$12:$D$36,2)"),
        ("Left after bills", "=G4-G5", "=H4-H5"),
        ("Even-out buffer", "=$B$5", "=-$B$5"),
        ("Left after evening out", "=G6+G7", "=H6+H7"),
        ("Surprise fund", "=-'Surprise Fund'!$B$22", "=-'Surprise Fund'!$B$22"),
        ("Groceries & gas", "=-$B$6", "=-$B$6"),
        ("Fun money", "=-$B$7", "=-$B$7"),
        ("TO YOUR GOAL", "=G8+G9+G10+G11", "=H8+H9+H10+H11")]
for i, (lab, a, b) in enumerate(rows):
    r = 4 + i; pp[f"F{r}"] = lab; pp[f"G{r}"] = a; pp[f"H{r}"] = b
    for c in "FGH": pp[f"{c}{r}"].border = thin; pp[f"{c}{r}"].font = F(bold=lab.isupper() or "Left" in lab)
    pp[f"G{r}"].number_format = pp[f"H{r}"].number_format = USD
for c in "FGH": pp[f"{c}12"].fill = PatternFill("solid", fgColor="D8F5E8")
pp["F14"] = "Per month to your goal (2 paychecks)"; pp["H14"] = "=G12+H12"; pp["H14"].number_format = USD; pp["F14"].font = pp["H14"].font = F(bold=True)
pp["F15"] = "Paid every 2 weeks = 26 paychecks a year, so twice a year a month has a 3rd paycheck: bills are already covered, so all of it can go to your goal."
pp["F15"].font = F(size=9, italic=True, color="6B7A8C"); pp["F15"].alignment = Alignment(wrap_text=True, vertical="top"); pp.merge_cells("F15:H17")
pp["F19"] = '=IF(MIN(G12:H12)<0,"⚠ A paycheck goes negative: move more buffer or trim groceries/fun.","✓ Both paychecks balance.")'; pp["F19"].font = F(bold=True, color=GREEN)
widths(pp, [40, 13, 15, 18, 3, 36, 14, 14])

# ------------------------------------------------------------- Surprise Fund
title(sf, "Surprise Fund", "Costs that happen every year, just not every month. Turn them into a bill.")
head(sf, 4, ["Irregular cost", "Per year"])
items = [("Holidays & gifts", 600), ("Car repairs", 500), ("Medical copays", 300), ("Car registration", 180), ("Annual subscriptions", 120)]
for r in range(5, 20):
    it = items[r - 5] if r - 5 < len(items) else (None, None)
    inp(sf.cell(r, 1), it[0]); inp(sf.cell(r, 2), it[1], USD)
sf["A21"] = "Total per year"; sf["B21"] = "=SUM(B5:B19)"
sf["A22"] = "Move to savings each paycheck (÷ 26, rounded up)"; sf["B22"] = "=ROUNDUP(B21/26,0)"
sf["A23"] = "Same thing, per month (÷ 12)"; sf["B23"] = "=B21/12"
for r in (21, 22, 23): sf[f"A{r}"].font = sf[f"B{r}"].font = F(bold=r != 23); sf[f"B{r}"].number_format = USD
sf["B22"].fill = PatternFill("solid", fgColor="D8F5E8")
sf["A25"] = "Tip: keep this money in a separate savings account so it doesn't get spent by accident."; sf["A25"].font = F(size=9, italic=True, color="6B7A8C")
widths(sf, [48, 14])

# ------------------------------------------------------------- Debt Payoff
title(dp, "Debt Payoff", "Choose a method; the schedule pays minimums on everything and sends every extra dollar to one target at a time.")
dp["A3"] = "Method"; inp(dp["B3"], "Avalanche")
dv = DataValidation(type="list", formula1='"Avalanche,Snowball"', allow_blank=False); dp.add_data_validation(dv); dv.add("B3")
dp["C3"] = "Avalanche = highest interest rate first (least interest). Snowball = smallest balance first (quick wins)."
dp["A4"] = "Monthly amount for debt"; dp["B4"] = "=SUM(D8:D13)+'Paycheck Plan'!H14"; style(dp["B4"], **INP); dp["B4"].number_format = USD
dp["C4"] = "Auto: all minimums + your monthly goal money from Paycheck Plan. Type over it to use your own number."
dp["A5"] = "Start month"; inp(dp["B5"], dt.date(2027, 1, 1), "mmm yyyy")
for r in (3, 4, 5): dp[f"A{r}"].font = F(bold=True); dp[f"C{r}"].font = F(size=9, italic=True, color="6B7A8C")
head(dp, 7, ["Debt", "Balance", "APR", "Minimum / month", "Order", "Paid off in (months)", "Minimum-only: months", "Minimum-only: interest", "calc"])
debts = [("Credit card", 3200, 0.24, 96)]
for j in range(6):
    r = 8 + j; d = debts[j] if j < len(debts) else (None, None, None, None)
    inp(dp.cell(r, 1), d[0]); inp(dp.cell(r, 2), d[1], USD); inp(dp.cell(r, 3), d[2], "0.0%"); inp(dp.cell(r, 4), d[3], USD)
    dp[f"E{r}"] = (f'=IF(A{r}="","",IF($B$3="Snowball",COUNTIFS($B$8:$B$13,"<"&B{r},$A$8:$A$13,"<>")+COUNTIFS($B$8:B{r},B{r},$A$8:A{r},"<>"),'
                   f'COUNTIFS($C$8:$C$13,">"&C{r},$A$8:$A$13,"<>")+COUNTIFS($C$8:C{r},C{r},$A$8:A{r},"<>")))')
    close = f"'Payoff Schedule'!{CL(3 + 5 * j + 4)}$4:{CL(3 + 5 * j + 4)}$363"
    dp[f"F{r}"] = f'=IF(A{r}="","",IF(COUNTIF({close},">0.005")>=360,"30+ years",COUNTIF({close},">0.005")+1))'
    dp[f"G{r}"] = f'=IF(A{r}="","",IFERROR(ROUNDUP(NPER(C{r}/12,-D{r},B{r}),0),"never"))'
    dp[f"H{r}"] = f'=IF(A{r}="","",IFERROR(NPER(C{r}/12,-D{r},B{r})*D{r}-B{r},"never"))'; dp[f"H{r}"].number_format = USD
    dp[f"I{r}"] = f'=IF(E{r}="",99,E{r})'; dp[f"I{r}"].font = F(size=8, color="A0A8B4")
    for c in "EFG": dp[f"{c}{r}"].alignment = Alignment(horizontal="center")
dp["A14"] = "Example row: the credit card from the video. Add up to 6 debts. List their minimums as bills on Paycheck Plan too."; dp["A14"].font = F(size=9, italic=True, color="6B7A8C")
res = [("Debt-free in (months)", '=IF(COUNT(B8:B13)=0,"",IF(COUNTIF(F8:F13,"30+ years")>0,"30+ years",MAX(F8:F13)))', "0"),
       ("Debt-free date", '=IF(ISNUMBER(B16),EDATE(B5,B16-1),"-")', "mmmm yyyy"),
       ("Total interest with this plan", "='Payoff Schedule'!AI2-SUM(B8:B13)", USD),
       ("Paying minimums only: months", '=IF(COUNTIF(G8:G13,"never")>0,"never",MAX(G8:G13))', "0"),
       ("Paying minimums only: interest (approx.)", '=IF(COUNTIF(H8:H13,"never")>0,"never",SUM(H8:H13))', USD),
       ("Interest you save", '=IF(ISNUMBER(B20),B20-B18,"-")', USD)]
for i, (lab, f, fmt) in enumerate(res):
    r = 16 + i; dp[f"A{r}"] = lab; dp[f"B{r}"] = f; dp[f"B{r}"].number_format = fmt
    dp[f"A{r}"].font = dp[f"B{r}"].font = F(bold=True); dp[f"A{r}"].border = dp[f"B{r}"].border = thin
for r in (16, 17, 21): dp[f"B{r}"].fill = PatternFill("solid", fgColor="D8F5E8")
dp["A23"] = '=IF(B4<SUM(D8:D13),"⚠ Monthly amount is less than your minimums. Raise it to at least "&TEXT(SUM(D8:D13),"$#,##0")&".","")'; dp["A23"].font = F(bold=True, color="C0392B")
widths(dp, [36, 14, 9, 16, 8, 18, 20, 22, 6])

# ------------------------------------------------------------- Payoff Schedule (the math)
sc["A1"] = "Payoff Schedule"; sc["A1"].font = F(bold=True, size=14, color=NAVY)
sc["A2"] = "Month by month. No inputs here; it reads the Debt Payoff tab."; sc["A2"].font = F(size=9, italic=True, color="6B7A8C")
sc["AH2"] = "Total paid:"; sc["AI2"] = "=SUM(AI4:AI363)"; sc["AI2"].number_format = USD2; sc["AH2"].font = sc["AI2"].font = F(bold=True)
hdr = ["Month", "Date"]
for j in range(6): hdr += [f"D{j+1} balance + interest", f"D{j+1} minimum", f"D{j+1} remaining", f"D{j+1} extra", f"D{j+1} end balance"]
hdr += ["Extra available", "Total end balance", "Paid this month"]
head(sc, 3, hdr)
for j in range(6):
    sc.cell(2, 3 + 5 * j, f"='Debt Payoff'!A{8+j}").font = F(bold=True, color="008000")
for r in range(4, 364):
    sc[f"A{r}"] = r - 3; sc[f"B{r}"] = f"=EDATE('Debt Payoff'!$B$5,A{r}-1)"; sc[f"B{r}"].number_format = "mmm yyyy"
    Mcells, cols = [], []
    for j in range(6):
        c0 = 3 + 5 * j; I, M, N, E, C = (CL(c0 + i) for i in range(5)); cols.append((I, M, N, E, C)); Mcells.append(f"{M}{r}")
        prev = f"N('Debt Payoff'!$B${8+j})" if r == 4 else f"{C}{r-1}"
        sc[f"{I}{r}"] = f"={prev}*(1+N('Debt Payoff'!$C${8+j})/12)"
        sc[f"{M}{r}"] = f"=MIN(N('Debt Payoff'!$D${8+j}),{I}{r})"
        sc[f"{N}{r}"] = f"={I}{r}-{M}{r}"
    pool = f"AG{r}"
    sc[pool] = f"=MAX(0,'Debt Payoff'!$B$4-SUM({','.join(Mcells)}))"
    for j, (I, M, N, E, C) in enumerate(cols):
        ahead = "+".join(f"('Debt Payoff'!$I${8+k}<'Debt Payoff'!$I${8+j})*{cols[k][2]}{r}" for k in range(6) if k != j)
        sc[f"{E}{r}"] = f"=MIN({N}{r},MAX(0,{pool}-({ahead})))"
        sc[f"{C}{r}"] = f"={I}{r}-{M}{r}-{E}{r}"
    sc[f"AH{r}"] = "=" + "+".join(f"{c[4]}{r}" for c in cols)
    sc[f"AI{r}"] = "=" + "+".join(f"{c[1]}{r}+{c[3]}{r}" for c in cols)
    for c in range(3, 36): sc.cell(r, c).number_format = USD2
for c in range(1, 36): sc.column_dimensions[CL(c)].width = 13
sc.freeze_panes = "C4"


# ------------------------------------------------------------- Paydays (3-paycheck months)
pd = wb.create_sheet("Paydays", 4)
title(pd, "Paydays", "Paid every two weeks? Find the months that bring a third paycheck.")
pd["A3"] = "Your first payday of the year"; pd["A3"].font = F(bold=True); inp(pd["B3"], dt.date(2027, 1, 1), "mmm d, yyyy")
pd["C3"] = "Enter the first payday that falls in the year you're planning. Every-two-weeks pay only."; pd["C3"].font = F(size=9, italic=True, color="6B7A8C")
head(pd, 6, ["#", "Payday"])
for k in range(27):
    r = 7 + k; pd[f"A{r}"] = k + 1
    pd[f"B{r}"] = f'=IF(YEAR($B$3+14*{k})=YEAR($B$3),$B$3+14*{k},"")'; pd[f"B{r}"].number_format = "ddd mmm d, yyyy"
pd["D6"] = "Month"; pd["E6"] = "Paydays"; pd["F6"] = ""
for c in "DEF": style(pd[f"{c}6"], **HEAD)
for m in range(12):
    r = 7 + m
    pd[f"D{r}"] = f"=DATE(YEAR($B$3),{m+1},1)"; pd[f"D{r}"].number_format = "mmmm"
    pd[f"E{r}"] = f'=COUNTIFS($B$7:$B$33,">="&D{r},$B$7:$B$33,"<"&EDATE(D{r},1))'; pd[f"E{r}"].alignment = Alignment(horizontal="center")
    pd[f"F{r}"] = f'=IF(E{r}>=3,"3 paychecks: extra check!","")'; pd[f"F{r}"].font = F(bold=True, color=GREEN)
from openpyxl.formatting.rule import FormulaRule
pd.conditional_formatting.add("D7:F18", FormulaRule(formula=["$E7>=3"], fill=PatternFill("solid", fgColor="D8F5E8")))
res2 = [("Paychecks this year", "=COUNT(B7:B33)", "0"), ("Months with 3 paychecks", '=COUNTIF(E7:E18,">=3")', "0"),
        ("Extra paychecks (beyond 2 a month)", "=E21-24", "0"), ("Extra money, at your take-home pay", "=E23*'Paycheck Plan'!B3", USD)]
for i, (lab, f, fmt) in enumerate(res2):
    r = 21 + i; pd[f"D{r}"] = lab; pd[f"E{r}"] = f; pd[f"E{r}"].number_format = fmt
    pd[f"D{r}"].font = pd[f"E{r}"].font = F(bold=True); pd[f"D{r}"].border = pd[f"E{r}"].border = thin
pd["E24"].fill = PatternFill("solid", fgColor="D8F5E8")
pd["D26"] = "Bills are already covered by the first two checks each month, so give each extra check a job before it lands."; pd["D26"].font = F(size=9, italic=True, color="6B7A8C")
widths(pd, [30, 22, 3, 36, 14, 28])

# ------------------------------------------------------------- Start Here content
title(st, "Paycheck Planner", "From the Paycheck Math channel · Budget by paycheck, not by month.")
steps = ["1. Paycheck Plan: enter your take-home pay and every bill with its due day. The sheet assigns each bill to a paycheck.",
         "2. Even them out: set the buffer (the sheet suggests an amount) so both paychecks leave about the same.",
         "3. Surprise Fund: list yearly costs (gifts, car repairs, renewals). It tells you what to set aside each paycheck.",
         "4. Debt Payoff: list your debts and pick Avalanche or Snowball. You get your debt-free date and the interest you save.",
         "5. Paydays: enter your first payday of the year to see which months bring a third paycheck."]
st["A4"] = "HOW TO USE"; st["A4"].font = F(bold=True, color=GREEN)
for i, s_ in enumerate(steps): st[f"A{5+i}"] = s_; st[f"A{5+i}"].font = F(); st[f"A{5+i}"].alignment = Alignment(wrap_text=True)
st["A11"] = "Legend:"; st["A11"].font = F(bold=True)
st["A12"] = "Yellow cells with blue text are yours to edit. Everything else calculates. Example values are from the video."; style(st["A12"], **INP)
st["A14"] = "YOUR NUMBERS"; st["A14"].font = F(bold=True, color=GREEN)
kp = [("Per month to your goal", "='Paycheck Plan'!H14", USD), ("Surprise fund per paycheck", "='Surprise Fund'!B22", USD),
      ("Debt-free in (months)", "='Debt Payoff'!B16", "0"), ("Debt-free date", "='Debt Payoff'!B17", "mmmm yyyy"),
      ("Interest saved vs. minimums", "='Debt Payoff'!B21", USD), ("Extra paychecks this year", "=Paydays!E23", "0")]
for i, (lab, f, fmt) in enumerate(kp):
    r = 15 + i; st[f"A{r}"] = lab; st[f"B{r}"] = f; st[f"B{r}"].number_format = fmt
    st[f"A{r}"].font = F(bold=True); st[f"B{r}"].font = F(bold=True, color="008000", size=13); st[f"A{r}"].border = st[f"B{r}"].border = thin
st["A22"] = "For education only, not financial advice. Results are estimates; your lender's actual interest and minimums may differ."; st["A22"].font = F(size=9, italic=True, color="6B7A8C")
widths(st, [100, 18])
for ws in wb.worksheets: fontall(ws); ws.sheet_view.showGridLines = ws.title == "Payoff Schedule"
pp.freeze_panes = "A12"
wb.save("Paycheck Planner.xlsx"); print("saved")
