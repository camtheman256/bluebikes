import * as functions from "firebase-functions/v1";
import * as admin from "firebase-admin";
import axios from "axios";
import * as fs from "fs";
import * as os from "os";

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
// export const helloWorld = functions.https.onRequest((request, response) => {
//   functions.logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

admin.initializeApp({
  storageBucket: "bluebikes-bbcc4.appspot.com",
});
const bucket = admin.storage().bucket();

export const fetchBluebikesData = functions.pubsub
  .schedule("every 1 hours synchronized")
  .onRun(async () => {
    const response = await axios.get(
      "https://gbfs.bluebikes.com/gbfs/en/station_status.json"
    );
    const filepath = os.tmpdir() + "/station_status.json";
    fs.writeFileSync(filepath, JSON.stringify(response.data));
    return bucket.upload(filepath, {
      destination: `status-${Date.now()}.json`,
    });
  });
