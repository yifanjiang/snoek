from snoek.activities.VoteTable import VoteTable
from snoek.activities.views import _toODSFile
from snoek.activities.views import _toODSTable
from snoek.activities.views import _hasVoted
from snoek.activities.models import *

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, TableColumnProperties, Map
from odf.number import NumberStyle, CurrencyStyle, CurrencySymbol,  Number,  Text
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

# def _toODSTable(v_table):
#     # generate an ods file to download
#     # input: VoteTable
#     # output: ods.table

#     doc= OpenDocumentSpreadsheet()
#     table= Table(name="Extremely Simple Table")

#     for cursorRow in v_table.table_with_row:
#         tr= TableRow()
#         table.addElement(tr)
#         td= TableCell()
#         td.addElement(P(text=cursorRow['row_head'].content))
#         tr.addElement(td)

#         for val in cursorRow['row_body']:
#             td= TableCell()
#             td.addElement(P(text=val))
#             tr.addElement(td)

#     doc.spreadsheet.addElement(table)
#     #myFile= tempfile.TemporaryFile('/tmp/')
#     doc.save('/tmp/test', True)

# vt_1 = VoteTable(1)
# vt_2 = VoteTable(2)
# vt_3 = VoteTable(3)
# vt_4 = VoteTable(4, 5) # 2D table

# ods_table = []

# ods_table.append(_toODSTable(vt_1))
# ods_table.append(_toODSTable(vt_2))
# ods_table.append(_toODSTable(vt_3))
# ods_table.append(_toODSTable(vt_4))

# _toODSFile(ods_table, 'myods')
usr = User.objects.get(pk = 6)
avt = Activity.objects.get(pk = 2)

print _hasVoted(usr, avt)

