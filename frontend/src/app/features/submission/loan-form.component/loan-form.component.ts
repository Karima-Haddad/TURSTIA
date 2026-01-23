import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-loan-form',
  imports: [ReactiveFormsModule],
  templateUrl: './loan-form.component.html',
  styleUrls: ['./loan-form.component.css']
})
export class LoanFormComponent {

  @Output() formChange = new EventEmitter<FormGroup>();

  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      loan_amount: [null, Validators.required],
      term_months: [null, Validators.required],
      product: ['Personal Loan'],
      purpose: ['']
    });

    this.form.valueChanges.subscribe(() => {
      this.formChange.emit(this.form);
    });
  }
  onSubmit() {
    if (this.form.valid) {
      console.log('Form submitted', this.form.value);
    } else {
      console.log('Form is invalid');
    }
  }
}
