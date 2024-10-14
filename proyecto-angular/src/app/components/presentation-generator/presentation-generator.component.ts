import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Observable, throwError } from 'rxjs';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, tap } from 'rxjs/operators';

interface PresentationRequest {
  msg: string;
  design: string;
  slides: number;
}

interface PresentationResult {
  pptx: string;
  pdf: string;
}

@Component({
  selector: 'app-presentation-generator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './presentation-generator.component.html',
  styleUrls: ['./presentation-generator.component.css']
})
export class PresentationGeneratorComponent {
  request: PresentationRequest = {
    msg: '',
    design: '',
    slides: 5
  };
  result: PresentationResult | null = null;
  isLoading: boolean = false;
  errorMessage: string | null = null;

  constructor(private http: HttpClient) {}

  onSubmit() {
    this.isLoading = true;
    this.errorMessage = null;
    this.result = null;

    const requestToSend: PresentationRequest = {
      msg: this.request.msg,
      design: this.request.design.toString(),
      slides: Number(this.request.slides)
    };

    this.generatePresentation(requestToSend)
      .subscribe(
        result => {
          this.result = result;
          this.isLoading = false;
        },
        error => {
          console.error('Error completo:', error);
          this.errorMessage = this.getErrorMessage(error);
          this.isLoading = false;
        }
      );
  }

  generatePresentation(request: PresentationRequest): Observable<PresentationResult> {
    console.log('Enviando solicitud:', request);
    return this.http.post<PresentationResult>('http://127.0.0.1:8000/presentation/generate', request)
      .pipe(
        tap(response => console.log('Respuesta recibida:', response)),
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    console.error('Error completo en handleError:', error);
    if (error.error instanceof ErrorEvent) {
      console.error('Error del cliente:', error.error.message);
    } else {
      console.error(
        `Backend retornó código ${error.status}, ` +
        `cuerpo era: ${JSON.stringify(error.error)}`);
    }
    return throwError(error);
  }

  private getErrorMessage(error: any): string {
    if (error instanceof HttpErrorResponse) {
      if (error.error && Array.isArray(error.error)) {
        return error.error.map(err => `${err.loc.join('.')}: ${err.msg}`).join('; ');
      } else if (error.error && error.error.detail) {
        return `Error: ${JSON.stringify(error.error.detail)}`;
      } else if (error.status === 422) {
        return 'Error de validación: Verifica que todos los campos estén correctamente llenados.';
      } else {
        return `Error del servidor: ${error.status} ${error.statusText}`;
      }
    }
    return 'Ocurrió un error desconocido. Por favor, intenta de nuevo.';
  }

  downloadFile(url: string, fileName: string) {
    this.isLoading = true;
    this.errorMessage = null;

    this.http.get(url, { responseType: 'blob' })
      .subscribe(
        (response: Blob) => {
          const blob = new Blob([response], { type: response.type });
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.download = fileName;
          link.click();
          window.URL.revokeObjectURL(downloadUrl);
          this.isLoading = false;
        },
        (error) => {
          console.error('Error al descargar el archivo:', error);
          this.errorMessage = 'Error al descargar el archivo. Por favor, intenta de nuevo.';
          this.isLoading = false;
        }
      );
  }

  downloadPptx() {
    if (this.result && this.result.pptx) {
      const fullUrl = `http://127.0.0.1:8000${this.result.pptx}`;
      console.log('URL completa del PPTX:', fullUrl);
      this.downloadFile(fullUrl, 'presentacion.pptx');
    } else {
      console.error('No se encontró la URL del archivo PPTX en el resultado');
      this.errorMessage = 'No se pudo encontrar el archivo PPTX para descargar.';
    }
  }
  
  downloadPdf() {
    if (this.result && this.result.pdf) {
      const fullUrl = `http://127.0.0.1:8000${this.result.pdf}`;
      console.log('URL completa del PDF:', fullUrl);
      this.downloadFile(fullUrl, 'presentacion.pdf');
    } else {
      console.error('No se encontró la URL del archivo PDF en el resultado');
      this.errorMessage = 'No se pudo encontrar el archivo PDF para descargar.';
    }
  }
}