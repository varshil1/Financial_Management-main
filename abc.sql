ALTER TABLE "Goals" 
DROP COLUMN "Goal_deadline";

ALTER TABLE "Goals" 
ADD COLUMN "Goal_deadline" date;


Select * from "Goals"

INSERT INTO "Goals"
VALUES(1,1,'new car',5000,3000,true,'2021-07-23')


INSERT INTO "Goals"
VALUES(2,1,'new bike',10000,2000,true,'2021-06-26');

Delete from "Goals" where "Goal_id"=5

INSERT INTO "Goals"
VALUES(2,1,'new bike',10000,2000,true,'2021-06-26');

INSERT INTO "Goals"
VALUES(3,1,'marriage',100000,20000,true,'2023-06-26');

INSERT INTO "Goals"
VALUES(4,1,'bicycle',1000,200,true,'2021-09-26');

INSERT INTO "Goals"
VALUES(5,1,'new mobile',30000,10000,false,'2022-06-26');

INSERT INTO "Goals"
VALUES(6,1,'Goa',20000,10000,true,'2022-06-26');

INSERT INTO "Goals"
VALUES(7,1,'ZNMD',40000,30000,true,'2022-06-26');


Select * from "expense"

delete from "expense"

INSERT INTO "expense"
VALUES(1,10000,'2021-03-30','rent',1,'paying the rent for march');


INSERT INTO "expense"
VALUES(1,1000,'2021-03-30','insurance',2,'insurance');

INSERT INTO "expense"
VALUES(1,2500,'2021-03-30','food',3,'pizza party');

INSERT INTO "expense"
VALUES(1,700,'2021-03-30','drink',4,'party for friends');

INSERT INTO "expense"
VALUES(1,8000,'2021-03-30','others',5,'friend birthday');


Select * from "income"

INSERT INTO "income"
VALUES(1,1,30000,'2021-03-30','salary');

INSERT INTO "income"
VALUES(2,1,10000,'2021-03-30','rent');

INSERT INTO "income"
VALUES(3,1,20000,'2021-03-30','allowance');

INSERT INTO "income"
VALUES(4,1,15000,'2021-03-30','bonus');

INSERT INTO "income"
VALUES(5,1,100000,'2021-03-30','business');

