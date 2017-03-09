import re
from bs4 import BeautifulSoup


DIV_INFO = {'name': "div",
            'attrs': {'style': "padding:7px;", 'align':"center"}}
DIV_SKILL = {'name': "div",
             'attrs': {'class': "contentModule phpGamesNonPortalView"}}
ID_ATT = """>Attack</a>"""
ID_SKILL = """** Spend Skill Points ***"""
ID_BEG = """Click here to begin the fight!"""
ID_LOOT = """ to see what you found!"""
ID_END = """Click here to return to the map"""


def parse_page(html):
    """determine what is happening in the game
    States: battle (fighting), map (moving), talk (talking)
    """
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**DIV_INFO)
    text = info.decode()

    # TODO: encounter battle state
    if ID_ATT in text:
        names = [e.next.next for e in info.find_all('font')]
        hp = re.findall("Health:.*?(\d+).*?(\d+)", text)[1:]
        return {'state': "attack", 'data': {'health': hp, 'names': names}}
    elif ID_BEG in text:
        return {'state': "begin_fight", 'data': None}
    elif ID_LOOT in text:
        # TODO: see if can shortcut past this without losing loot
        return {'state': "loot", 'data': None}
    elif ID_END in text:
        return {'state': "end_fight", 'data': None}
    elif ID_SKILL in text:
        return {'state': "skill", 'data': None}
    else:
        return {'state': "map", 'data': None}


def parse_skills(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**DIV_SKILL)
    text = info.decode()


def page_trim(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    info = parsed_html.body.find(**DIV_SKILL)
    return info.decode()


"""Examples:
Battle:
<div align="center" style="padding:7px;">Name: <b>Isaac_Pereire</b> | Level: <b>2</b> | Health: <b>29</b>/30 <img height="10" src="http://images.neopets.com/nq/n/exp_green.gif" width="96"><img height="10" src="http://images.neopets.com/nq/n/exp_gray.gif" width="4"><br>Experience: <b>1,126</b> <img height="10" src="http://images.neopets.com/nq/n/exp_gold.gif" width="66"><img height="10" src="http://images.neopets.com/nq/n/exp_gray.gif" width="34"> | Difficulty: <b>Normal</b><br><br><table border="0" cellpadding="2" width="540"><tr><td align="center" valign="bottom" width="270"><img src="http://images.neopets.com/nq/n/lupe_combat.gif"/></td><td align="center" valign="bottom" width="270"><img src="http://images.neopets.com/nq/m/400001_asnowimp.gif"/></td></tr><tr><td colspan="2"> <br/></td></tr><tr><td align="center" bgcolor="#00ff00"><font size="+1"><b>Isaac_Pereire</b></font></td><td align="center" bgcolor="#ff9999"><font size="+1"><b>A snow imp</b></font></td></tr><tr>
<td align="left" valign="top">Health: <b>29</b>/30 <img height="10" src="http://images.neopets.com/nq/n/exp_green.gif" width="96"><img height="10" src="http://images.neopets.com/nq/n/exp_gray.gif" width="4"><br>Weapon: <b>White Wand</b><br>Armour: <b>none</b><br/></br></br></img></img></td>
<td align="left" valign="top">Health: <b>10</b>/10 <img height="10" src="http://images.neopets.com/nq/n/exp_green.gif" width="100"><img height="10" src="http://images.neopets.com/nq/n/exp_gray.gif" width="0"><br>Level: <b>1</b><br/></br></img></img></td>
</tr>
<tr><td colspan="2"><img height="2" src="http://images.neopets.com/nq/blank.gif"/></td></tr><script type="text/javascript"><!--
var ff_submit = 0;function setdata(id1, id2) {	document.ff.fact.value = id1;	document.ff.type.value = id2;	if (ff_submit == 0) {ff_submit = 1;		document.ff.submit();	}}
function setfact(id) {	document.ff.fact.value = id;}
function settype(id) {	document.ff.type.value = id;}
function do_submit() {	if (ff_submit == 0) {		ff_submit = 1;		document.ff.submit();	}}
// --></script><form action="neoquest.phtml" method="post" name="ff"><input name="fact" type="hidden" value=""><input name="type" type="hidden" value=""/></input></form><tr><td bgcolor="#9999ff" colspan="2"><a href="javascript:;" onclick="setdata('attack', 0); return false;">Attack</a><br>
<br><a href="javascript:;" onclick="setdata('flee', 0); return false;">Flee</a><br>
<a href="javascript:;" onclick="setdata('noop', 0); return false;">Do nothing</a><br>
</br></br></br></br></td></tr></table>
</br></br></img></img></br></img></img></div>




SKILL:
<div class="contentModule phpGamesNonPortalView"><div class="frame"><div class="contentModuleHeader">
			<b>NeoQuest</b>
			</div>
			<div align="center" style="padding:7px;">Name: <B>b__madoff</B> | Level: <B>2</B> | Health: <B>30</B>/30 <IMG SRC="http://images.neopets.com/nq/n/exp_green.gif" HEIGHT="10" WIDTH="100"><IMG SRC="http://images.neopets.com/nq/n/exp_gray.gif" HEIGHT="10" WIDTH="0"><BR>Experience: <B>796</B> <IMG SRC="http://images.neopets.com/nq/n/exp_gold.gif" HEIGHT="10" WIDTH="25"><IMG SRC="http://images.neopets.com/nq/n/exp_gray.gif" HEIGHT="10" WIDTH="75"> | Difficulty: <B>Normal</B><BR><BR><B><FONT SIZE="+5">SPEND SKILL POINTS</FONT></B><BR><BR>You currently have <B>1</B> skill point left to spend.<BR>Click on the question marks (?) to get information about specific skills.<BR><BR><FONT COLOR="ff0000">Red</FONT> skills are skills that you are allowed to spend a skill point in.<BR>Remember, you can only spend a skill point in a skill if you have MORE skill points in the previous skill.  For example, if your <B>Firepower</B> skill is at 2, and your <B>Fire Weapons</B> skill is at 3, you can spend one point in <B>Firepower</B>, but you can't spend another until you improve <B>Fire Weapons</B> another point.  The first skill in a skill tree doesn't have any prerequisites, so you can always raise those as high as you want (to the skill limit of 10) without improving another skill first.<BR><BR><TABLE BORDER="0"><TR><TD VALIGN="top"><TABLE BORDER="0"><TR><TD COLSPAN="2"><B><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#1', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A>  Fire Magic</B></TD></TR><TR><TD WIDTH="130" BGCOLOR="#ffff80">- <I>Skill Name</I></TD><TD WIDTH="40" ALIGN="center" BGCOLOR="#ffff80"><I>Level</I></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#1001', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <A HREF="neoquest.phtml?skill_choice=1001&action=skill"><FONT COLOR="#ff0000">Fire Weapons</TD><TD ALIGN="center">-</A></FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#1002', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Firepower</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#1003', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Fire Ball</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#1004', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Wall of Flame</TD><TD ALIGN="center">-</FONT></TD></TR></TABLE></TD><TD VALIGN="top"><TABLE BORDER="0"><TR><TD COLSPAN="2"><B><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#2', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A>  Ice Magic</B></TD></TR><TR><TD WIDTH="130" BGCOLOR="#ffff80">- <I>Skill Name</I></TD><TD WIDTH="40" ALIGN="center" BGCOLOR="#ffff80"><I>Level</I></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#2001', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <A HREF="neoquest.phtml?skill_choice=2001&action=skill"><FONT COLOR="#ff0000">Ice Weapons</TD><TD ALIGN="center">-</A></FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#2002', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Heart of Ice</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#2003', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Snowball</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#2004', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Glacier Strike</TD><TD ALIGN="center">-</FONT></TD></TR></TABLE></TD><TD VALIGN="top"><TABLE BORDER="0"><TR><TD COLSPAN="2"><B><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#3', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A>  Shock Magic</B></TD></TR><TR><TD WIDTH="130" BGCOLOR="#ffff80">- <I>Skill Name</I></TD><TD WIDTH="40" ALIGN="center" BGCOLOR="#ffff80"><I>Level</I></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#3001', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <A HREF="neoquest.phtml?skill_choice=3001&action=skill"><FONT COLOR="#ff0000">Shock Weapons</TD><TD ALIGN="center">-</A></FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#3002', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Disable</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#3003', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Fortitude</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#3004', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Shockwave</TD><TD ALIGN="center">-</FONT></TD></TR></TABLE></TD></TR><TR><TD VALIGN="top"><TABLE BORDER="0"><TR><TD COLSPAN="2"><B><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#4', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A>  Spectral Magic</B></TD></TR><TR><TD WIDTH="130" BGCOLOR="#ffff80">- <I>Skill Name</I></TD><TD WIDTH="40" ALIGN="center" BGCOLOR="#ffff80"><I>Level</I></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#4001', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <A HREF="neoquest.phtml?skill_choice=4001&action=skill"><FONT COLOR="#ff0000">Spectral Weapons</TD><TD ALIGN="center">-</A></FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#4002', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Evasion</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#4003', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Absorption</TD><TD ALIGN="center">-</FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#4004', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Reflex</TD><TD ALIGN="center">-</FONT></TD></TR></TABLE></TD><TD VALIGN="top"><TABLE BORDER="0"><TR><TD COLSPAN="2"><B><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#5', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A>  Life Magic</B></TD></TR><TR><TD WIDTH="130" BGCOLOR="#ffff80">- <I>Skill Name</I></TD><TD WIDTH="40" ALIGN="center" BGCOLOR="#ffff80"><I>Level</I></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#5001', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <A HREF="neoquest.phtml?skill_choice=5001&action=skill"><FONT COLOR="#ff0000">Life Weapons</TD><TD ALIGN="center"><B>3</B></A></FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#5002', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <A HREF="neoquest.phtml?skill_choice=5002&action=skill"><FONT COLOR="#ff0000">Field Medic</TD><TD ALIGN="center"><B>2</B></A></FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#5003', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <FONT COLOR="#000000">Lifesteal</TD><TD ALIGN="center"><B>2</B></FONT></TD></TR><TR><TD><A HREF="javascript:;" ONCLICK="window.open('nq_skills.phtml#5004', 'skillinfo', 'height=400,width=400,resizable=yes,scrollbars=yes'); return false;">?</A> <A HREF="neoquest.phtml?skill_choice=5004&action=skill"><FONT COLOR="#ff0000">Resurrection</TD><TD ALIGN="center">-</A></FONT></TD></TR></TABLE></TD></TABLE></div></div></div><div style="clear:both"></div><BR><BR><CENTER><FORM ACTION="neoquest.phtml" METHOD="post"><INPUT TYPE="submit" VALUE="Click here to return to the map"></FORM></CENTER></div></div></div><div style="clear:both"></div><br clear="all">

									</td>
			</tr>
		</table>
	</div>
"""
