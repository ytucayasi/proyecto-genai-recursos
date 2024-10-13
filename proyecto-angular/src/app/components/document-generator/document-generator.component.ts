import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface DocumentData {
  malla_curricular: string;
  silabo: string;
  rubricas: string;
  tema: string;
}

@Component({
  selector: 'app-document-generator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './document-generator.component.html',
  styleUrls: ['./document-generator.component.css']
})
export class DocumentGeneratorComponent {
  malla_curricular: string = '';
  silabo: string = '';
  rubricas: string = '';
  tema: string = '';
  loading: boolean = false;

  constructor(private http: HttpClient) {}

  async onSubmit(): Promise<void> {
    this.loading = true;

    const documentData: DocumentData = {
      malla_curricular: this.malla_curricular,
      silabo: this.silabo,
      rubricas: this.rubricas,
      tema: this.tema
    };

    try {
      const response = await this.http.post('http://127.0.0.1:8000/documents/generate_word', documentData).toPromise();
      console.log('Documento generado:', response);
    } catch (error) {
      console.error('Error al generar el documento:', error);
    } finally {
      this.loading = false;
    }
  }
}
