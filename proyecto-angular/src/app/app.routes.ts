import { Routes } from '@angular/router';
import { EvaluationGeneratorComponent } from './components/evaluation-generator/evaluation-generator.component';
import { DocumentGeneratorComponent } from './components/document-generator/document-generator.component';
import { PresentationGeneratorComponent } from './components/presentation-generator/presentation-generator.component';

export const routes: Routes = [
    { path: 'evaluation-generator', component: EvaluationGeneratorComponent },
    { path: '', redirectTo: '/evaluation-generator', pathMatch: 'full' },
    { path: 'document-generator', component: DocumentGeneratorComponent },
    { path: '', redirectTo: '/document-generator', pathMatch: 'full' },
    { path: 'presentation-generator', component: PresentationGeneratorComponent }
];