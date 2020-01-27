#$language = "VBScript"
#$interface = "1.0"

crt.Screen.Synchronous = True

' This automatically generated script may need to be
' edited in order to work correctly.

Sub Main
    crt.Dialog.MessageBox("Script is running​")
    i=1
    do while i>0
        crt.Screen.Send "date" & chr(13)
        crt.Sleep 1500000
    loop
End Sub
