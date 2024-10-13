import { Component, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface Question {
  tipo: string;
  pregunta: string;
  opciones?: string[];
  respuesta_correcta?: number | boolean;
  respuesta_sugerida?: string;
}

interface Evaluation {
  preguntas: Question[];
}

@Component({
  selector: 'app-evaluation-generator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: 'evaluation-generator.component.html',
  styleUrl: 'evaluation-generator.component.css'
})
export class EvaluationGeneratorComponent {
  files = signal<File[]>([]);
  numQuestions = signal(5);
  numOptions = signal(4);
  difficulty = signal(0);
  type = signal(0);
  evaluation = signal<Evaluation | null>(null);
  loading = signal(false);

  constructor(private http: HttpClient) { }

  onFileChange(event: any): void {
    this.files.set(Array.from(event.target.files));
  }

  updateNumQuestions(value: number) {
    this.numQuestions.set(value);
  }

  updateNumOptions(value: number) {
    this.numOptions.set(value);
  }

  updateDifficulty(value: number) {
    this.difficulty.set(value);
  }

  updateType(value: number) {
    this.type.set(value);
  }

  async onSubmit(): Promise<void> {
    this.loading.set(true);
    const formData = new FormData();
    this.files().forEach(file => formData.append('files', file));
    formData.append('numero_preguntas', this.numQuestions().toString());
    formData.append('numero_opciones', this.numOptions().toString());
    formData.append('dificultad', this.difficulty().toString());
    formData.append('tipo', this.type().toString());

    try {
      const response = await this.http.post<{ evaluation: Evaluation }>('http://localhost:8000/cuestionario/generate_evaluation', formData).toPromise();
      this.evaluation.set(response!.evaluation);
    } catch (error) {
      console.error('Error al generar la evaluación:', error);
    } finally {
      this.loading.set(false);
    }
  }
}