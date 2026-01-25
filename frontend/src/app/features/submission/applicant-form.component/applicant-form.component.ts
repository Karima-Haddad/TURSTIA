import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-applicant-form',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './applicant-form.component.html',
  styleUrls: ['./applicant-form.component.css']
})
export class ApplicantFormComponent {

  @Output() formChange = new EventEmitter<FormGroup>();

  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      age: [null, Validators.required],
      employment_type: ['', Validators.required],
      monthly_income_declared: [null, Validators.required],
      monthly_expenses_declared: [null, Validators.required],
      sector: ['', Validators.required],
      late_payments_declared: [0]
    });

    this.form.valueChanges.subscribe(() => {
      this.formChange.emit(this.form);
    });
  }
}
