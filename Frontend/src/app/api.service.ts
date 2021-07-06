import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MessageModel } from './message.model';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  //lastMessage='';
  //https://medbaybot-api.herokuapp.com/postMessage
  //https://medbaybot-api.herokuapp.com/getDiseaseInfo
  getUrl:string = "http://192.168.43.110:4200/";
  postUrl:string = "http://192.168.0.9:5000/postMessage";
  diseaseUrl:string = "http://192.168.0.9:5000/getDiseaseInfo";
  constructor(private http:HttpClient) { }
  sendMessage(message) {
    let headers = new HttpHeaders();
    headers = headers.append('Accept', 'text/plain');
    headers = headers.append('Content-type', 'application/json');
    return this.http.post <MessageModel>(this.postUrl,message,{headers})
  }
  getDiseaseInfo(message){
    let headers = new HttpHeaders();
    headers = headers.append('Accept', 'text/plain');
    headers = headers.append('Content-type', 'application/json');
    return this.http.post(this.diseaseUrl,message,{headers})
  }
 /*  getMessage(){
    return this.http.get(this.getUrl)
  } */
}
