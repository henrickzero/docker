import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Adicione esta linha
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RoboComponent } from './robo/robo.component';

@NgModule({
  declarations: [
    AppComponent,
    RoboComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule, // Adicione esta linha
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
