Option Explicit

Dim AccessApp, dbPath, outputSqlPath, sqlConnectionString, rs, sqlFile
Dim strSQL, exportSQL

' Параметры
dbPath = "E:\RinHack\DB.accdb" ' Путь к вашей БД Access
outputSqlPath = "E:\RinHach\db.sql" ' Путь для сохранения SQL файла
sqlConnectionString = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" & dbPath

' Создаем экземпляр приложения Access
Set AccessApp = CreateObject("Access.Application")
AccessApp.OpenCurrentDatabase dbPath

' Создаем объект для работы с ADO
Set rs = CreateObject("ADODB.Recordset")

' Получаем название всех таблиц в базе данных
strSQL = "SELECT * FROM MSysObjects WHERE Type=1 AND Flags=0"
rs.Open strSQL, AccessApp.CurrentDb

Set sqlFile = CreateObject("Scripting.FileSystemObject").OpenTextFile(outputSqlPath, 2, True)

' Экспортируем каждую таблицу в SQL
Do Until rs.EOF
    Dim tableName
    tableName = rs.Fields("Name").Value

    exportSQL = "SELECT * INTO " & tableName & " FROM [" & tableName & "];" & vbCrLf
    sqlFile.WriteLine exportSQL

    rs.MoveNext
Loop

' Закрываем все
sqlFile.Close
rs.Close
AccessApp.Quit

Set rs = Nothing
Set sqlFile = Nothing
Set AccessApp = Nothing

WScript.Echo "Экспорт завершен!"