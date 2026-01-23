import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ApplicationService {

  private API_URL = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  submitApplication(payload: any) {
    return this.http.post(
      `${this.API_URL}/submit-application`,
      payload
    );
  }
}
