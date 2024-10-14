import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface Document {
  tema: string;
  malla_curricular: string;
  silabo: string;
  rubricas: string;
  id: number;
  content: string;
  ruta: string;
}

@Component({
  selector: 'app-document-generator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './document-generator.component.html',
  styleUrls: ['./document-generator.component.css']
})
export class DocumentGeneratorComponent implements OnInit {
  malla_curricular: string = '';
  silabo: string = '';
  rubricas: string = '';
  tema: string = '';
  loading: boolean = false;
  documents: Document[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.getDocuments();
  }

  getDocuments(): void {
    this.http.get<Document[]>('http://127.0.0.1:8000/documents').subscribe(
      (response) => {
        this.documents = response;
      },
      (error) => {
        console.error('Error al obtener documentos:', error);
      }
    );
  }

  async onSubmit(): Promise<void> {
    this.loading = true;

    const documentData = {
      malla_curricular: this.malla_curricular,
      silabo: this.silabo,
      rubricas: this.rubricas,
      tema: this.tema
    };

    try {
      const response = await this.http.post('http://127.0.0.1:8000/documents/generate_word', documentData).toPromise();
      console.log('Documento generado:', response);
      // Recargar la página después de generar el documento
      window.location.reload();
    } catch (error) {
      console.error('Error al generar el documento:', error);
    } finally {
      this.loading = false;
    }
  }

  downloadFile(ruta: string): void {
    const filename = ruta.split('/').pop()!;
    this.http.get(`http://127.0.0.1:8000/documents/download/${filename}`, { responseType: 'blob' })
      .subscribe(
        (blob: Blob) => {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = filename;
          link.click();
          window.URL.revokeObjectURL(url);
        },
        (error) => {
          console.error('Error al descargar el archivo:', error);
        }
      );
  }
}
