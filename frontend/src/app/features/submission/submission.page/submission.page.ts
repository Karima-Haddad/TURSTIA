import { Component, ViewChild } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ApplicationService } from '../../../services/application.service';
import { v4 as uuidv4 } from 'uuid';

import { ApplicantFormComponent } from '../applicant-form.component/applicant-form.component';
import { LoanFormComponent } from '../loan-form.component/loan-form.component';
import { DocumentUploadComponent } from '../document-upload.component/document-upload.component';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-submission',
  standalone: true,
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
  documentResult: any = null;

  constructor(private applicationService: ApplicationService,
    private http: HttpClient) {}

  onApplicantFormChange(form: FormGroup) {
    this.applicantForm = form;
  }

  onLoanFormChange(form: FormGroup) {
    this.loanForm = form;
  }

  onDocumentsUpdate(docs: any[]) {
    this.documents = docs;
  }

  generateCaseId(prefix: string = "APP"): string {
    const today = new Date();
    const dateStr = today.toISOString().slice(0,10).replace(/-/g, ""); // YYYYMMDD

    // Récupérer le compteur depuis localStorage (ou backend si tu veux persistant)
    const key = `case_counter_${dateStr}`;
    let counter = Number(localStorage.getItem(key) || 0);
    counter += 1;
    localStorage.setItem(key, counter.toString());

    // Formater sur 4 chiffres
    const counterStr = counter.toString().padStart(4, "0");

    return `${prefix}-${dateStr}-${counterStr}`;
  }
  
  formSubmitted = false;

  submit() {
    this.formSubmitted = true;

    if (!this.applicantForm || !this.loanForm) {
      console.log("Forms not ready");
      return;
    }

    if (this.applicantForm.invalid || this.loanForm.invalid || this.documents.length === 0) {
      console.log("⛔ Form invalid");
      return;
    }

    if (this.documents.length === 0) {
      console.log("⛔ No documents");
      return;

    }

    console.log("📎 Documents avant envoi :", this.documents);
    const applicationPackage = {
      case_id: this.generateCaseId(),
      submitted_at: new Date().toISOString(),
      applicant_form: this.applicantForm?.value,
      loan_request: this.loanForm?.value,
      documents: this.documents  // contient maintenant content base64
    };

    console.log("📤 Payload envoyé :", applicationPackage);
    
    this.http.post<any>('http://127.0.0.1:8000/api/complete-evaluation',
    applicationPackage).subscribe(
      res => {
        console.log("✅ TEST POST Response:", res);
        this.documentResult = res;
      },
      err => {
        console.error("❌ TEST POST Error:", err);
      }
    );

  }
}