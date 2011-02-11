from snoek.activities.models import *
from snoek.activities.Voter import Voter
from django.contrib.auth.models import User


class VoteTable:

    def __init__(self, v_id_row = 0, v_id_col = 0):
        self.v_id_row = v_id_row
        self.v_id_col = v_id_col
        self.voters = self._getVoterList()
        self.title = self.getTableTitle()
        self.row_head = self.getTableRowHead()
        self.col_head = self.getTableColHead()
        self.table_with_row = self.getTableWithRow()
        self.table_body = self.getTableBody()
        self.user_table = self.getUserTable()        

    def is2D(self):
        # return True if this is a 2D table
        return self.v_id_row and self.v_id_col

    def isValidate(self):
        # TODO        
        # Validate the input of v_ids for 2D table
        # The 2 votes should have the same user set.
        return True      

    def getTableTitle(self):

        if self.is2D():
            return Vote.objects.get(id = self.v_id_row).summary + '.VS.' + Vote.objects.get(id = self.v_id_col).summary
        else:
            return Vote.objects.get(id = self.v_id_row).summary
        
    def getTableRowHead(self):
        # Row Head is a list of Questions        
        # [Object Question, Object Question, Object Question, Object Question,]
        
        row = []
        for q in Question.objects.filter(vote = self.v_id_row):
            row.append(q)
        return row

    def getTableColHead(self):
        # Col head is a list of Questions
        # [Object Question, Object Question, Object Question, Object Question,]
        
        col = []
        for q in Question.objects.filter(vote = self.v_id_col):
            col.append(q)
        return col
            
    def getTableWithRow(self):
        # Get a table body with row information - for rendering convenience
        #
        # 
        # [
        # 
        #   { 'row_head' : Object Question}, { 'row_body' : [value01, value02, ...]}
        #   { 'row_head' : Object Question}, { 'row_body' : [value11, value12, ...]}
        #   { 'row_head' : Object String3}, { 'row_body' : [value21, value22, ...]}
        #   { 'row_head' : Object String4}, { 'row_body' : [value31, value32, ...]}
        #   
        #   ...
        #   
        # ]
        #
        # For 1D table, the value pair for 'row_body' is a list with only one
        # element.

        table = []
        rowbody = []
        if not self.is2D():
        # generate 1D table
            for q in self.row_head:
                rowbody.append(q.answernumber)
                table.append({'row_head': q, 'row_body': rowbody})
                rowbody = []
        else:
        # generate 2D table
            # the first row - column heads
            # table.append({'row_head': 'HEAD of TABLE', 'row_body': self.col_head})
            # Construct an empty table with all cell's value 0
            for q in self.row_head:
                for c in self.col_head:
                    rowbody.append(0)            # fill up data in the empty table
                table.append({'row_head': q, 'row_body': rowbody})
                rowbody = []

            # for u in User.objects.all():
            for u in self.voters:
                voter = Voter(u.id)
                for c_q in self.col_head:
                    for r_q in self.row_head:                    
                        col_answer = voter.getAnswerOfQuestion(c_q)
                        row_answer = voter.getAnswerOfQuestion(r_q)
                        if (not col_answer == False) and (not row_answer == False):
                            row_index = self.row_head.index(row_answer.question)
                            col_index = self.col_head.index(col_answer.question)
                            table[row_index]['row_body'][col_index] = table[row_index]['row_body'][col_index] + 1
                            continue
        return table

    def getTableBody(self):
        # Get a table body without row / head information
        #
        # [
        #
        #   [value01, value02, ...]
        #   [value11, value22, ...]
        #   [value31, value32, ...]        
        #
        #   ...
        #
        # ]
        tb = []
        for row in self.table_with_row:
            tb.append(row['row_body'])
        return tb

    def getUserTable(self):
        # table structure is a list of dictionaries:
        #
        # 
        # [
        # 
        #   { 'row_head' : Object User, 'row_body' : [value01, value02, ...]},
        #   { 'row_head' : Object User, 'row_body' : [value11, value12, ...]},
        #   { 'row_head' : Object User, 'row_body' : [value21, value22, ...]},
        #   
        #   ...
        #   
        # ]

        table = []
        rowbody = []
        answers = []
        v = Vote.objects.get(pk = self.v_id_row)

        for q in v.question_set.all():
            answers = answers + list(q.answer_set.all())

        for a in answers:
            for c in self.row_head:
                if a.question == c:
                    rowbody.append(1)
                else:
                    rowbody.append(0)
            table.append({'row_head': a.user, 'row_body': rowbody})
            rowbody = []
        return table    


    def _getVoterList(self):

        ul = []
        v = Vote.objects.get(pk=self.v_id_row)
        
        for q in v.question_set.all():
            for a in q.answer_set.all():
                ul.append(a.user)
                
        return ul
