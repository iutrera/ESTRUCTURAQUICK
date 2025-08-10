Attribute VB_Name = "Module2"
Sub built_model_LL()

Dim objOpenSTAAD As Object
'Launch OpenSTAAD Object
Set objOpenSTAAD = GetObject(, "StaadPro.OpenSTAAD")

objOpenSTAAD.View.SelectGroup ("_external-LL")


disttotranslationrep = ThisWorkbook.Sheets("INITIALIZE").Cells(17, 4).Value
Dim varLinkBays As Double
Dim varOpenBase As Double
Dim varAxisDir As Integer
Dim varSpacingArray(1) As Double
Dim varNoBays As Integer
Dim varRenumberBay As Double
Dim varRenumberArray(0) As Integer
Dim varGeometryOnly As Double

    varLinkBays = 0
    varOpenBase = 1
    varAxisDir = 1
    varSpacingArray(0) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(1) = 1 * CDbl(disttotranslationrep)
   ' varSpacingArray(2) = 1 * CDbl(disttotranslationrep)

    varRenumberArray(0) = 1

    varNoBays = 2
    varRenumberBay = 0
    varGeometryOnly = 0
Dim lNodeCount As Long
Dim bretval As Boolean

bretval = objOpenSTAAD.Geometry.DoTranslationalRepeat(varLinkBays, varOpenBase, varAxisDir, varSpacingArray, varNoBays, varRenumberBay, varRenumberArray, varGeometryOnly)

objOpenSTAAD.Geometry.ClearMemberSelection

Set objOpenSTAAD = Nothing

End Sub

Sub built_model_W()

Dim objOpenSTAAD As Object
'Launch OpenSTAAD Object
Set objOpenSTAAD = GetObject(, "StaadPro.OpenSTAAD")

objOpenSTAAD.View.SelectGroup ("_external-W1")
objOpenSTAAD.View.SelectGroup ("_external-W2")

disttotranslationrep = ThisWorkbook.Sheets("INITIALIZE").Cells(18, 4).Value
Dim varLinkBays As Double
Dim varOpenBase As Double
Dim varAxisDir As Integer
Dim varSpacingArray(2) As Double
Dim varNoBays As Integer
Dim varRenumberBay As Double
Dim varRenumberArray(0) As Integer
Dim varGeometryOnly As Double

    varLinkBays = 0
    varOpenBase = 1
    varAxisDir = 0
    varSpacingArray(0) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(1) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(2) = 1 * CDbl(disttotranslationrep)

    varRenumberArray(0) = 1

    varNoBays = 3
    varRenumberBay = 0
    varGeometryOnly = 0
Dim lNodeCount As Long
Dim bretval As Boolean

bretval = objOpenSTAAD.Geometry.DoTranslationalRepeat(varLinkBays, varOpenBase, varAxisDir, varSpacingArray, varNoBays, varRenumberBay, varRenumberArray, varGeometryOnly)

objOpenSTAAD.Geometry.ClearMemberSelection

Set objOpenSTAAD = Nothing

End Sub


Sub built_model_LR()

Dim objOpenSTAAD As Object
'Launch OpenSTAAD Object
Set objOpenSTAAD = GetObject(, "StaadPro.OpenSTAAD")

objOpenSTAAD.View.SelectGroup ("_external-LR")


disttotranslationrep = ThisWorkbook.Sheets("INITIALIZE").Cells(17, 4).Value
Dim varLinkBays As Double
Dim varOpenBase As Double
Dim varAxisDir As Integer
Dim varSpacingArray(1) As Double
Dim varNoBays As Integer
Dim varRenumberBay As Double
Dim varRenumberArray(0) As Integer
Dim varGeometryOnly As Double

    varLinkBays = 0
    varOpenBase = 1
    varAxisDir = 1
    varSpacingArray(0) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(1) = 1 * CDbl(disttotranslationrep)
   ' varSpacingArray(2) = 1 * CDbl(disttotranslationrep)

    varRenumberArray(0) = 1

    varNoBays = 2
    varRenumberBay = 0
    varGeometryOnly = 0
Dim lNodeCount As Long
Dim bretval As Boolean

bretval = objOpenSTAAD.Geometry.DoTranslationalRepeat(varLinkBays, varOpenBase, varAxisDir, varSpacingArray, varNoBays, varRenumberBay, varRenumberArray, varGeometryOnly)

objOpenSTAAD.Geometry.ClearMemberSelection
Set objOpenSTAAD = Nothing

End Sub

Sub built_windwall1()

Dim objOpenSTAAD As Object
'Launch OpenSTAAD Object
Set objOpenSTAAD = GetObject(, "StaadPro.OpenSTAAD")

objOpenSTAAD.View.SelectGroup ("_windwall1")


disttotranslationrep = ThisWorkbook.Sheets("INITIALIZE").Cells(18, 4).Value * -1
Dim varLinkBays As Double
Dim varOpenBase As Double
Dim varAxisDir As Integer
Dim varSpacingArray(2) As Double
Dim varNoBays As Integer
Dim varRenumberBay As Double
Dim varRenumberArray(0) As Integer
Dim varGeometryOnly As Double

    varLinkBays = 0
    varOpenBase = 1
    varAxisDir = 0
    varSpacingArray(0) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(1) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(2) = 1 * CDbl(disttotranslationrep)

    varRenumberArray(0) = 1

    varNoBays = 3
    varRenumberBay = 0
    varGeometryOnly = 0
Dim lNodeCount As Long
Dim bretval As Boolean

bretval = objOpenSTAAD.Geometry.DoTranslationalRepeat(varLinkBays, varOpenBase, varAxisDir, varSpacingArray, varNoBays, varRenumberBay, varRenumberArray, varGeometryOnly)

objOpenSTAAD.Geometry.ClearMemberSelection
Set objOpenSTAAD = Nothing

End Sub

Sub built_windwall2()

Dim objOpenSTAAD As Object
'Launch OpenSTAAD Object
Set objOpenSTAAD = GetObject(, "StaadPro.OpenSTAAD")

objOpenSTAAD.View.SelectGroup ("_windwall2")


disttotranslationrep = ThisWorkbook.Sheets("INITIALIZE").Cells(18, 4).Value
Dim varLinkBays As Double
Dim varOpenBase As Double
Dim varAxisDir As Integer
Dim varSpacingArray(2) As Double
Dim varNoBays As Integer
Dim varRenumberBay As Double
Dim varRenumberArray(0) As Integer
Dim varGeometryOnly As Double

    varLinkBays = 0
    varOpenBase = 1
    varAxisDir = 0
    varSpacingArray(0) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(1) = 1 * CDbl(disttotranslationrep)
    varSpacingArray(2) = 1 * CDbl(disttotranslationrep)

    varRenumberArray(0) = 1

    varNoBays = 3
    varRenumberBay = 0
    varGeometryOnly = 0
Dim lNodeCount As Long
Dim bretval As Boolean

bretval = objOpenSTAAD.Geometry.DoTranslationalRepeat(varLinkBays, varOpenBase, varAxisDir, varSpacingArray, varNoBays, varRenumberBay, varRenumberArray, varGeometryOnly)

objOpenSTAAD.Geometry.ClearMemberSelection
Set objOpenSTAAD = Nothing

End Sub


Sub built_model()

Call built_model_LL
Call built_model_W
Call built_model_LR
Call built_windwall1
Call built_windwall2

End Sub

