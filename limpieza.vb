Sub EliminarTB()
Dim celda As Range
Dim rango As Range

On Error Resume Next
    Set rango = Application.InputBox("Seleccionar rango a limpiar", Type:=8)
On Error GoTo 0
    If rango Is Nothing Then Exit Sub
    For Each celda In rango
        If celda.Font.Color = RGB(255, 255, 255) Then celda.ClearContents
Next celda

End Sub