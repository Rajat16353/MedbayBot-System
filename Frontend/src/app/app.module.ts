import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { HttpClientModule } from '@angular/common/http';
import { MessagesComponent } from './messages/messages.component';
import { UserInputComponent } from './user-input/user-input.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { SymptomsComponent } from './symptoms/symptoms.component';
import { DrugInfoComponent } from './messages/drug-info/drug-info.component';
import { DiseaseInfoComponent } from './messages/disease-info/disease-info.component';
import { SafePipe } from './safe.pipe';

@NgModule({
  declarations: [
    AppComponent,
    MessagesComponent,
    UserInputComponent,
    SymptomsComponent,
    DrugInfoComponent,
    DiseaseInfoComponent,
    SafePipe
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FlexLayoutModule,
    FontAwesomeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
