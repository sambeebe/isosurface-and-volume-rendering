import vtk
import math


class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self,parent=None):
        self.timer_count = 0
        self.parent = vtk.vtkRenderWindowInteractor()

    def execute(self,obj,event):

      self.actor.SetPosition(self.timer_count, self.timer_count,0);
      key = self.parent.GetKeySym()
      self.timer_count += .25
      rep.PushPlane((math.sin(self.timer_count*1.1)*17.))
      rep.GetPlane(plane)
      renwin.Render()


# UNCOMMENT THIS TO ENABLE ANIMATION
# interactor.AddObserver('TimerEvent', cb.execute)



planeWidget = vtk.vtkImplicitPlaneWidget2()


#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("/Users/sambeebe/vis-2019/assignment-4-sambeebe/data/brain.vtk")
imageReader.Update()

#create an outline that shows the bounds of our dataset
outline = vtk.vtkOutlineFilter();
outline.SetInputConnection(imageReader.GetOutputPort());

#mapper to push the outline geometry to the graphics library
outlineMapper = vtk.vtkPolyDataMapper();
outlineMapper.SetInputConnection(outline.GetOutputPort());

#actor for the outline to add to our renderer
outlineActor = vtk.vtkActor();
outlineActor.SetMapper(outlineMapper);
outlineActor.GetProperty().SetLineWidth(4.0);

renwin = vtk.vtkRenderWindow()
txt = vtk.vtkTextActor()

interactor = vtk.vtkRenderWindowInteractor()
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetBlendModeToComposite()
volumeMapper.SetInputConnection(imageReader.GetOutputPort())

volumeColor = vtk.vtkColorTransferFunction()
volumeColor.AddRGBPoint(0.,.23,.29,.75)
volumeColor.AddRGBPoint(27.,.4,.533,.9333)
volumeColor.AddRGBPoint(60.,.865,.865,.865)
volumeColor.AddRGBPoint(69.,.917,.38313,.3784314)
volumeColor.AddRGBPoint(205.,.968,.686,.572)
volumeColor.AddRGBPoint(255,.706,.0156,.14902)


volumeScalarOpacity = vtk.vtkPiecewiseFunction()
volumeScalarOpacity.AddPoint(0.,0.)
volumeScalarOpacity.AddPoint(25,0.)
volumeScalarOpacity.AddPoint(40.,0.747)
volumeScalarOpacity.AddPoint(65.9,.818)
volumeScalarOpacity.AddPoint(74.,1.)
volumeScalarOpacity.AddPoint(81.,0.)
volumeScalarOpacity.AddPoint(255.,1.)



volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(volumeColor)
volumeProperty.SetScalarOpacity(volumeScalarOpacity)

volumeProperty.SetInterpolationTypeToLinear()

#timer stuff for animation
actor = vtk.vtkActor()
cb = MyInteractorStyle()
cb.actor = actor

timerId = interactor.CreateRepeatingTimer(100);

volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

plane = vtk.vtkPlane()

def myCallback(obj, event):
  global plane
  obj.GetRepresentation().GetPlane(plane)

rep = vtk.vtkImplicitPlaneRepresentation()
rep.SetPlaceFactor(1.525)
rep.PlaceWidget(outlineActor.GetBounds())
rep.SetNormal(plane.GetNormal())

renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)


#The render window
volume.GetMapper().AddClippingPlane(plane)
renwin.SetSize(1028, 800);
renwin.AddRenderer(renderer)

renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(180);


interactor.SetRenderWindow(renwin)
planeWidget.SetInteractor(interactor)
planeWidget.AddObserver("InteractionEvent",myCallback);
planeWidget.SetRepresentation(rep)

planeWidget.On()
interactor.Initialize()
interactor.Start()
