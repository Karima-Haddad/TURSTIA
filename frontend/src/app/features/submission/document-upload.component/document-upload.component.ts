import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-document-upload',
  imports: [CommonModule],
  templateUrl: './document-upload.component.html',
  styleUrls: ['./document-upload.component.css']
})
export class DocumentUploadComponent {

  @Output() documentsChange = new EventEmitter<any[]>();

  documents: any[] = [];

  onFileSelected(event: any, type: string) {
    const file = event.target.files[0];
    if (!file) return;

    // Simulation upload (backend viendra après)
    const fakeUri = `uploads/${file.name}`;

    this.documents.push({
      doc_id: 'D' + (this.documents.length + 1),
      type: type,
      uri: fakeUri
    });

    this.documentsChange.emit(this.documents);
  }
}
