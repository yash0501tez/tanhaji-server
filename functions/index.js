const functions = require("firebase-functions");
const express = require("express");
const admin = require("firebase-admin");
const app = express();
const cors = require("cors");
const { Buffer } = require("buffer");
const { InMemorySigner } = require("@taquito/signer");
const {
  char2Bytes,
  bytes2Char,
  verifySignature,
  validateSignature,
  buf2hex,
} = require("@taquito/utils");
const { TezosToolkit, RpcPacker } = require("@taquito/taquito");
const {
  Parser,
  packDataBytes,
  packData,
  MichelsonData,
  MichelsonType,
} = require("@taquito/michel-codec");

const Signer = new InMemorySigner(
  "edskRneBSS17e9BX3tMf7PbdcmDwuPJJAcpGYz3F1NvUVvzJYpWHBBdACiW4hR1U5PQSFAxjFbjED5njLoRkqYxjL5hhFa1o9n"
);

const serviceAccount = require("../serviceAccountKey.json");

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://tantest-35456-default-rtdb.firebaseio.com",
});

const tezos = new TezosToolkit("https://ghostnet.smartpy.io/").setProvider({
  signer: Signer,
});

const db = admin.database();

app.use(cors({ origin: true }));

app.get("/", (req, res) => {
  res.send("Hello World Firebase");
});

app.post("/create_sign", async (req, res) => {
  const { userid, address, amount, token_id } = req.body;

  const data = `(Pair (Pair "${address}" ${amount}) ${token_id})`;
  const type = `(pair (pair (address) (nat)) (nat))`;

  const p = new Parser();
  const dataJSON = p.parseMichelineExpression(data);
  const typeJSON = p.parseMichelineExpression(type);

  const packed = packDataBytes(dataJSON, typeJSON);
  console.log(packed);

  const signature = await Signer.sign(packed.bytes);
  console.log(signature);

  // res.status(200).json({
  //   message: "Signature created",
  //   signature: signature,
  // });

  const userRef = db.ref("users/");
  const newUserRef = userRef.push();
  newUserRef
    .set({
      userid: userid,
      address: address,
      signature: signature,
      amount: amount,
      token_id: token_id,
    })
    .then((result) => {
      console.log(result);
      res.status(200).json({
        message: "Signature created",
        signature: signature,
        result: result,
      });
    })
    .catch((error) => {
      console.log(error);
      res.status(500).json({
        message: "Error creating signature",
        error: error,
      });
    });
});

app.post("/create_sign_with_cid", async(req, res)=>{
  const {address, token_id} = req.body;

  let ipfs_cid = "ipfs://bafkreiatkozctcbvb7zcfehl7ydrd3ucdg47r6cnpszelzuhqpulc2zlgq"

  const p = new Parser();
  const ipfs_cid_bytes = char2Bytes(ipfs_cid);

  console.log(ipfs_cid_bytes)

  const data = `(Pair (Pair "${address}" ${token_id}) "${ipfs_cid_bytes}")`;
  const type = `(pair (pair (address) (nat)) (bytes))`;

  const dataJSON = p.parseMichelineExpression(data);
  const typeJSON = p.parseMichelineExpression(type);

  const packed = packDataBytes(dataJSON, typeJSON);
  console.log(packed);

  const signature = await Signer.sign(packed.bytes);
  console.log(signature);

  try{
    res.status(200).json({
      message: "Signature created",
      signature: signature,
    });
  }catch(err){
    console.log(err)
    res.status(500).json({
      message: "Error creating signature",
      error: err,
    });
  }
})

app.post("/create_nft_sign", async(req, res)=>{
  const { address, token_id  } = req.body;

  // bafkreieebbnr4xmpdj5ud3evwswbnppq6sv3tdelbw5cyldjfqz76fub3y  img link

  const p = new Parser();

  const name = "Sword NFT";
  const description = "This is a sword NFT";
  const decimals = 0;
  const artifactUri = "https://bafkreieebbnr4xmpdj5ud3evwswbnppq6sv3tdelbw5cyldjfqz76fub3y.ipfs.nftstorage.link/"
  const displayUri = "https://bafkreieebbnr4xmpdj5ud3evwswbnppq6sv3tdelbw5cyldjfqz76fub3y.ipfs.nftstorage.link/"
  const thumbnailUri = "https://bafkreieebbnr4xmpdj5ud3evwswbnppq6sv3tdelbw5cyldjfqz76fub3y.ipfs.nftstorage.link/"

  const nameBytes = char2Bytes(name);
  const descriptionBytes = char2Bytes(description);
  const artifactUriBytes = char2Bytes(artifactUri);
  const displayUriBytes = char2Bytes(displayUri);
  const thumbnailUriBytes = char2Bytes(thumbnailUri);

  // console.log(metadata)

  // const data = `(Pair (Pair "${address}" ${token_id}) ${artifactUriBytes})`;
  // const type = `(pair (pair (address) (nat)) (bytes))`;

  // const data = `(Pair ( Pair ( Pair "${address}" ${token_id} ) ( Pair "${nameBytes}" "${descriptionBytes}" ) ) ( Pair ( Pair "${artifactUriBytes}" "${displayUriBytes}" ) "${thumbnailUriBytes}" ) )`;
  // const type = `(pair (pair (pair (address) (nat)) (pair (bytes) (bytes))) (pair (pair (bytes) (bytes)) (bytes)))`;

  const data = `(Pair "${address}" (Pair ${token_id} (Pair "${nameBytes}" (Pair "${descriptionBytes}" (Pair "${artifactUriBytes}" (Pair "${displayUriBytes}" "${thumbnailUriBytes}"))))))`;
  const type = `(pair (address) (pair (nat) (pair (bytes) (pair (bytes) (pair (bytes) (pair (bytes) (bytes)))))))`;

  // const data = 
  // `(Pair 
  //   "${address}" 
  //   (Pair 
  //     ${token_id} 
  //     (Pair 
  //       "${nameBytes}" 
  //       (Pair 
  //         "${descriptionBytes}" 
  //         (Pair 
  //           "${artifactUriBytes}" 
  //           (Pair 
  //             "${displayUriBytes}" 
  //             "${thumbnailUriBytes}"
  //           )
  //         )
  //       )
  //     )
  //   )
  // )`;
  // const type = 
  // `(pair 
  //   (address) 
  //   (pair 
  //     (nat) 
  //     (pair 
  //       (bytes) 
  //       (pair 
  //         (bytes) 
  //         (pair 
  //           (bytes) 
  //           (pair 
  //             (bytes) 
  //             (bytes)
  //           )
  //         )
  //       )
  //     )
  //   )
  // )`;

  console.log(data)

  const dataJSON = p.parseMichelineExpression(data);
  const typeJSON = p.parseMichelineExpression(type);

  const packed = packDataBytes(dataJSON, typeJSON);
  console.log(packed.bytes);
  // console.log(typeof packed.bytes);

  const data_bytes = "0507070a000000160000fadcd216de7817afb85f7f7a39510e2ed22430320707000007070a0000000953776f7264204e465407070a000000135468697320697320612073776f7264204e465407070a0000005968747470733a2f2f6261666b726569656562626e7234786d70646a357564336576777377626e707071367376337464656c62773563796c646a66717a373666756233792e697066732e6e667473746f726167652e6c696e6b2f07070a0000005968747470733a2f2f6261666b726569656562626e7234786d70646a357564336576777377626e707071367376337464656c62773563796c646a66717a373666756233792e697066732e6e667473746f726167652e6c696e6b2f0a0000005968747470733a2f2f6261666b726569656562626e7234786d70646a357564336576777377626e707071367376337464656c62773563796c646a66717a373666756233792e697066732e6e667473746f726167652e6c696e6b2f"

  const signature = await Signer.sign(packed.bytes);
  // const signature = await Signer.sign(data_bytes);
  console.log(signature);

  try{
    res.status(200).json({
      message: "Signature created",
      signature: signature,
      data: data_bytes,
    })
  }
  catch(error){
    console.log(error);
    res.status(500).json({
      message: "Error creating signature",
      error: error,
    });
  }
})

app.get("/get_sign", async (req, res) => {
  const { userid } = req.query;
  const userRef = db.ref("users/" + userid);
  userRef
    .once("value", (snapshot) => {
      const user = snapshot.val();
      console.log(user);
      res.status(200).json({
        message: "Signature retrieved",
        user: user,
      });
    })
    .catch((error) => {
      console.log(error);
      res.status(500).json({
        message: "Error retrieving signature",
        error: error,
      });
    });
});

exports.widgets = functions.https.onRequest(app);
