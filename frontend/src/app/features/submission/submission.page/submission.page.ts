import { Component } from '@angular/core';
import { FormGroup, ReactiveFormsModule  } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApplicationService } from '../../../services/application.service';

import { ApplicantFormComponent } from '../applicant-form.component/applicant-form.component';
import { LoanFormComponent } from '../loan-form.component/loan-form.component';
import { DocumentUploadComponent } from '../document-upload.component/document-upload.component';

@Component({
  selector: 'app-submission',
  imports: [
    CommonModule,
    ApplicantFormComponent,
    LoanFormComponent,
    DocumentUploadComponent,
    ReactiveFormsModule
  ],
  templateUrl: './submission.page.html',
  styleUrls: ['./submission.page.css']
})
export class SubmissionPage {

  applicantForm!: FormGroup;
  loanForm!: FormGroup;
  documents: any[] = [];

  onApplicantFormChange(form: FormGroup) {
    this.applicantForm = form;
  }

  onLoanFormChange(form: FormGroup) {
    this.loanForm = form;
  }

  onDocumentsUpdate(docs: any[]) {
    this.documents = docs;
  }

  constructor(private appService: ApplicationService) {}

  submit() {
    const payload = {
      applicant_form: this.applicantForm.value,
      loan_request: this.loanForm.value,
      documents: this.documents
    };

    this.appService.submitApplication(payload)
      .subscribe(res => {
        console.log('Backend response:', res);
      });
  }

}
