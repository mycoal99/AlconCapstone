class Patient:

    def __init__(self, patient_id, firstname, lastname, DOB, left_eye_template, right_eye_template, surgery):
        self.patient_id = patient_id
        self.firstname = firstname
        self.lastname = lastname
        self.DOB = DOB
        self.left_eye_template = left_eye_template
        self.right_eye_template = right_eye_template
        self.surgery = surgery

    # @property
    # def patient_id(self):
    #     return '{}'.format(self.patient_id)

    # @property
    # def fullname(self):
    #     return '{} {}'.format(self.firstname, self.lastname)

    # @property
    # def date_of_birth(self):
    #     return '{}'.format(self.date_of_birth)

    # @property
    # def eye_template(self):
    #     return '{}'.format(self.eye_template)