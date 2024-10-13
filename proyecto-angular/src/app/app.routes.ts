import { Routes } from '@angular/router';
import { EvaluationGeneratorComponent } from './components/evaluation-generator/evaluation-generator.component';

export const routes: Routes = [
    { path: 'evaluation-generator', component: EvaluationGeneratorComponent },
    { path: '', redirectTo: '/evaluation-generator', pathMatch: 'full' }
];