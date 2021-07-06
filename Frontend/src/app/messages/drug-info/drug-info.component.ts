import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from 'src/app/api.service';
import { BotMessageService } from 'src/app/bot-message.service';

@Component({
  selector: 'app-drug-info',
  templateUrl: './drug-info.component.html',
  styleUrls: ['./drug-info.component.scss']
})
export class DrugInfoComponent implements OnInit {
  @Input() drugList;
  showFullSideEffect = false;
  showFullUses = false;
  showFullInfo = false;
  constructor(private botMessageService:BotMessageService, private apiService:ApiService) { }

  ngOnInit() {
    if(this.drugList.drug_info.side_effect){
      this.botMessageService.drugInfo = false;
    }
    
  }

  getDrugData(link:string,name:string){
    let messageForBot = {
      "name":this.botMessageService.username,
      "age":this.botMessageService.age,
      "gender":this.botMessageService.gender,
      "text":"",
      "selected_drug_link":link
    }
    this.botMessageService.messages.push({message:name,symptoms:[],owner:'user'})
      this.botMessageService.messagesChanged.next(this.botMessageService.messages);
      this.apiService.sendMessage(messageForBot).subscribe((res)=>{
        this.botMessageService.generateBotMessage(res);
      });
  }


}
