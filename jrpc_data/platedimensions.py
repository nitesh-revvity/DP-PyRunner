class PlateDimensions:
	def __init__(self, WellsX=None, WellsY=None, Height=None, WellDiameterBottom=None, WellDiameterTop=None, CornerWell1X=None, CornerWell1Y=None, CornerWell2X=None, CornerWell2Y=None, CornerWell3X=None, CornerWell3Y=None, CornerWell4X=None, CornerWell4Y=None, WellShapeBottom=None, WellShapeTop=None, WellDepth=None, FlangeHeight=None, IsProtrusionVisible=None, PlateColor=None):
		self.type = "PlateDimensions:#PerkinElmer.Mmd"
		self.WellsX = WellsX
		self.WellsY = WellsY
		self.Height = Height
		self.WellDiameterBottom = WellDiameterBottom
		self.WellDiameterTop = WellDiameterTop
		self.CornerWell1X = CornerWell1X
		self.CornerWell1Y = CornerWell1Y
		self.CornerWell2X = CornerWell2X
		self.CornerWell2Y = CornerWell2Y
		self.CornerWell3X = CornerWell3X
		self.CornerWell3Y = CornerWell3Y
		self.CornerWell4X = CornerWell4X
		self.CornerWell4Y = CornerWell4Y
		self.WellShapeBottom = WellShapeBottom
		self.WellShapeTop = WellShapeTop
		self.WellDepth = WellDepth
		self.FlangeHeight = FlangeHeight
		self.IsProtrusionVisible = IsProtrusionVisible
		self.PlateColor = PlateColor
