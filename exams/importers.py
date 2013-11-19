# -*- coding: utf-8 -*-
from lxml import etree

class Candidate(object):

    XML_SUBJECT_FIELDS = (
        'MAS_PAK1', # äidinkieli A, O, I, Z, W | A5
        'MAS_PAK2', # pakollinen
        'MAS_PAK3', # pakollinen
        'MAS_PAK4', # pakollinen
        'MAS_YAK1', # ylimääräinen
        'MAS_YAK2',
        'MAS_YAK3',
        'MAS_YAK4',
        'MAS_YAK5',
        'MAS_YAK6',
    )
    def __init__(self, id=None, identity_number=None, ctype=None, gender=None, school=None, examination=None, retrying=None, batch=None, subjects=[], *args, **kwargs):
        self._settings = kwargs

        if id:
            self.id = id
        if gender:
            self.gender = gender
        if school:
            self.school = school
        if ctype:
            self.ctype = ctype
        if identity_number:
            self.identity_number = identity_number
        if examination:
            self.examination = examination
        if retrying:
            self.retrying = retrying
        if batch:
            self.batch = batch

    @property
    def examination(self):
        return self._examination
    @examination.setter
    def examination(self, value):
        self._examination = value
    
    @property
    def identity_number(self):
        return self._identity_number
    @identity_number.setter
    def identity_number(self, value):
        self._identity_number = value
    
    
    @property
    def retrying(self):
        return self._retrying
    @retrying.setter
    def retrying(self, value):
        if value == 'U':
            val = True
        elif value == None:
            val = False
        else:
            raise ValueError
        self._retrying = val
    

    @property
    def gender(self):
        return self._gender
    @gender.setter
    def gender(self, value):
        val = int(value)
        if val in (1, 2):
            self._gender = val
        else:
            raise ValueError, 'Invalid gender %s' % value

    @property
    def ctype(self):
        return self._ctype
    @ctype.setter
    def ctype(self, value):
        self._ctype = value
    

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def subjects(self):
        return self._subjects
    @subjects.setter
    def subjects(self, value):
        self._subjects = value
    
    @property
    def school(self):
        return self._school
    @school.setter
    def school(self, value):
        self._school = value

    @property
    def batch(self):
        return self._batch
    @batch.setter
    def batch(self, value):
        self._batch = value
    
    
    def parse_xml(self, xmltree):
        if isinstance(xmltree, etree._Element):
            self.id = int(xmltree.xpath('MAS_KOKELASNUMERO')[0].text)
            self.ctype = int(xmltree.xpath('MAS_KOLKOODI')[0].text)
            self.examination = xmltree.xpath('MAS_TKETUNNUS')[0].text
            self.school = int(xmltree.xpath('MAS_LUKIONRO')[0].text)
            self.gender = int(xmltree.xpath('MAS_SUKUPUOLI')[0].text)
            self.identity_number = xmltree.xpath('MAS_KKEHETU')[0].text
            try:
                self.retrying = xmltree.xpath('MAS_UUSIJA')[0].text
            except IndexError:
                self.retrying = None
            self.batch = xmltree.xpath('MAS_ERA')[0].text
            subjects = []
            for field in self.XML_SUBJECT_FIELDS:
                res = xmltree.xpath(field)
                if len(res) > 0:
                    subject = res[0].text
                    subjects.append(subject)
            self.subjects = subjects
        else:
            raise ValueError


def parse_candidate_xml(filename):
    candidates = []

    with open(filename, 'r') as xmlfile:
        try:
            root = etree.parse(xmlfile)
        except etree.XMLSyntaxError:
            return False

        rows = root.xpath('/ROWSET/ROW')

        for row in rows:
            candidate = Candidate()
            candidate.parse_xml(row)
            candidates.append(candidate)

    return candidates