#ViewBox Changer
from bs4 import BeautifulSoup
from re import sub

class ChangeViewBox:
	svgPosAttrX = ['width', 'x', 'cx', 'rx']
	svgPosAttrY = ['height', 'y', 'cy', 'ry']
	svgPosVar = ['points', 'd']
	# these are neutral measures (because they affect both x and y axis), so I chose to calculate their average.
	svgPosNeutral = ['stroke-width', 'r']
	# 0 = x and 1 = y
	pos = 0
	def __init__(self, xml: str, svg: bool) -> None:
		if svg:
			self.soup = BeautifulSoup(xml, 'lxml-xml')
			self.viewbox = self.soup.svg['viewBox'].strip()
			self.tags = self.soup.svg.find_all()
	def Transform(self, number, before, after) -> float:
		return float(after)*float(number)/float(before)
	def PosVar(self, match) -> float:
		if self.pos == 0:
			self.pos = 1
			return self.Transform(match, self.xvb, self.xnvb)
		else:
			self.pos = 0
			return self.Transform(match, self.yvb, self.ynvb)
	def cvb(self, nvb: str) -> None:
		self.xvb = self.viewbox.split()[2]
		self.yvb = self.viewbox.split()[3]
		self.xnvb = nvb.strip().split()[0]
		self.ynvb = nvb.strip().split()[1]
		self.soup.svg['viewBox'] = f'{self.Transform(self.viewbox.split()[0], self.xvb, self.xnvb)} {self.Transform(self.viewbox.split()[1], self.yvb, self.ynvb)} {self.xnvb} {self.ynvb}'
		for tag in self.tags:
			for i in tag.attrs.keys():
				if i in self.svgPosVar:
					tag[i] = sub(r'[-+]?\d*\.\d+|\d+', lambda m: f'{self.PosVar(m.group())}' ,tag[i])
				elif i in self.svgPosAttrX:
					tag[i] = str(self.Transform(tag[i], self.xvb, self.xnvb))
				elif i in self.svgPosAttrY:
					tag[i] = str(self.Transform(tag[i], self.yvb, self.ynvb))
				elif i in self.svgPosNeutral:
					tag[i] = str((self.Transform(tag[i], self.xvb, self.xnvb) + self.Transform(tag[i], self.yvb, self.ynvb))/2)
				
	def __str__(self) -> str:
		return str(self.soup)

		
