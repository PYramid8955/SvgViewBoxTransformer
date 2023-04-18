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
			self.viewbox = self.soup.svg['viewBox']
			self.tags = self.soup.svg.find_all()
	def Transform(self, number: float, before: float, after: float) -> float:
		return after*number/before
	def PosVar(self, match: float) -> float:
		if self.pos == 0:
			self.pos = 1
			return self.Transform(match, float(self.xvb), float(self.xnvb))
		else:
			self.pos = 0
			return self.Transform(match, float(self.yvb), float(self.ynvb))
	def cvb(self, nvb: str) -> None:
		self.soup.svg['viewBox'] = nvb.strip()
		self.xvb = self.viewbox.split()[2]
		self.yvb = self.viewbox.split()[3]
		self.xnvb = nvb.split()[2]
		self.ynvb = nvb.split()[3]
		for tag in self.tags:
			for i in tag.attrs.keys():
				if i in self.svgPosVar:
					tag[i] = sub(r'[-+]?\d*\.\d+|\d+', lambda m: f'{self.PosVar(float(m.group()))}' ,tag[i])
				elif i in self.svgPosAttrX:
					tag[i] = str(self.Transform(float(tag[i]), float(self.xvb), float(self.xnvb)))
				elif i in self.svgPosAttrY:
					tag[i] = str(self.Transform(float(tag[i]), float(self.yvb), float(self.ynvb)))
				elif i in self.svgPosNeutral:
					tag[i] = str((self.Transform(float(tag[i]), float(self.xvb), float(self.xnvb)) + self.Transform(float(tag[i]), float(self.yvb), float(self.ynvb)))/2)
				
	def __str__(self) -> str:
		return str(self.soup)

		
