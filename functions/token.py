import smartpy as sp
FA2 = sp.io.import_script_from_url("https://smartpy.io/templates/fa2_lib.py")

class Sword_Token(
    FA2.Admin, 
    FA2.ChangeMetadata,
    FA2.WithdrawMutez, 
    FA2.MintNft, 
    FA2.BurnNft, 
    FA2.OnchainviewBalanceOf, 
    FA2.Fa2Nft):
        
    def __init__(
        self, 
        admin, 
        metadata, 
        token_metadata = {}, 
        ledger = {}, 
        policy = None, 
        metadata_base = None):
            
        FA2.Fa2Nft.__init__(
            self, 
            metadata, 
            token_metadata = token_metadata, 
            ledger = ledger, 
            policy = policy, 
            metadata_base = metadata_base
        )
        FA2.Admin.__init__(self, admin)
        
    @sp.entry_point
    def mint(self, sig, data_bytes, data):
        sp.set_type(sig, sp.TSignature)
        sp.set_type(data_bytes, sp.TBytes)
        sp.set_type(
            data, 
            sp.TRecord(
                address = sp.TAddress,
                token_id = sp.TNat,
                name = sp.TBytes,
                description = sp.TBytes,
                artifact_uri = sp.TBytes,
                display_uri = sp.TBytes,
                thumbnail_uri = sp.TBytes
            ).layout(("address", ("token_id", ("name", ("description", ("artifact_uri", ("display_uri", "thumbnail_uri")))))))
        )

        data_pack = sp.pack(data)

        sp.verify(data_bytes == data_pack, message = "Data is not valid")
        
        k = sp.key("edpkuKYJd4SMv4eyxeQ7CDnL43XMu7itdVvjUNgowWLTrm5YtFa5Qt")

        sp.verify(
            sp.check_signature(k, sig, data_pack), 
            message = "Signature is not valid"
        )
        
        # const data = `(Pair ( Pair ( Pair "${address}" ${token_id} ) ( Pair "${nameBytes}" "${descriptionBytes}" ) ) ( Pair ( Pair "${artifactUriBytes}" "${displayUriBytes}" ) "${thumbnailUriBytes}" ) )`;

        # data = sp.unpack(
        #     data_bytes,
        #     sp.TPair(
        #         sp.TPair(
        #             sp.TPair(
        #                 sp.TAddress,
        #                 sp.TNat
        #             ),
        #             sp.TPair(
        #                 sp.TBytes,
        #                 sp.TBytes
        #             )
        #         ),
        #         sp.TPair(
        #             sp.TPair(
        #                 sp.TBytes,
        #                 sp.TBytes
        #             ),
        #             sp.TBytes
        #         )
        #     )
        # )

        # const data = `(Pair "${address}" (Pair ${token_id} (Pair "${nameBytes}" (Pair "${descriptionBytes}" (Pair "${artifactUriBytes}" (Pair "${displayUriBytes}" "${thumbnailUriBytes}"))))))`;

        sp.trace(data_bytes)
        sp.trace(
            sp.unpack(
                data_bytes,
                sp.TRecord(
                    address = sp.TAddress,
                    token_id = sp.TNat,
                    name = sp.TBytes,
                    description = sp.TBytes,
                    artifact_uri = sp.TBytes,
                    display_uri = sp.TBytes,
                    thumbnail_uri = sp.TBytes
                ).layout(("address", ("token_id", ("name", ("description", ("artifact_uri", ("display_uri", "thumbnail_uri")))))))
            ).open_some("Invalid data_bytes")
        )

        data = sp.compute(
            sp.unpack(
                data_bytes,
                sp.TRecord(
                    address = sp.TAddress,
                    token_id = sp.TNat,
                    name = sp.TBytes,
                    description = sp.TBytes,
                    artifact_uri = sp.TBytes,
                    display_uri = sp.TBytes,
                    thumbnail_uri = sp.TBytes
                ).layout(("address", ("token_id", ("name", ("description", ("artifact_uri", ("display_uri", "thumbnail_uri")))))))
                # add an error message in open_some() if data_bytes is not valid
            ).open_some("Invalid data_bytes")
        )

        

        address = data.address
        token_id = data.token_id
        name = data.name
        description = data.description
        artifact_uri = data.artifact_uri
        display_uri = data.display_uri
        thumbnail_uri = data.thumbnail_uri

        # data = sp.compute(
        #     sp.unpack(
        #         data_bytes,
        #         sp.TPair(
        #             sp.TAddress,
        #             sp.TPair(
        #                 sp.TNat,
        #                 sp.TPair(
        #                     sp.TBytes,
        #                     sp.TPair(
        #                         sp.TBytes,
        #                         sp.TPair(
        #                             sp.TBytes,
        #                             sp.TPair(
        #                                 sp.TBytes,
        #                                 sp.TBytes
        #                             )
        #                         )
        #                     )
        #                 )
        #             )
        #         )
        #     ).open_some()
        # )

        # address = sp.fst(sp.fst(data.open_some()))
        # amount = sp.snd(sp.fst(data.open_some()))
        # token_id = sp.snd(data.open_some())

        # address = sp.fst(data)
        # token_id = sp.fst(sp.snd(data))
        # name = sp.fst(sp.snd(sp.snd(data)))
        # description = sp.fst(sp.snd(sp.snd(sp.snd(data))))
        # artifact_uri = sp.fst(sp.snd(sp.snd(sp.snd(sp.snd(data)))))
        # display_uri = sp.fst(sp.snd(sp.snd(sp.snd(sp.snd(sp.snd(data))))))
        # thumbnail_uri = sp.snd(sp.snd(sp.snd(sp.snd(sp.snd(sp.snd(data))))))
        
        # address = sp.fst(sp.fst(sp.fst(data.open_some())))
        # # token_id = sp.snd(sp.fst(sp.fst(data.open_some())))
        # name = sp.fst(sp.snd(sp.fst(data.open_some())))
        # description = sp.snd(sp.snd(sp.fst(data.open_some())))
        # artifact_uri = sp.fst(sp.fst(sp.snd(data.open_some())))
        # display_uri = sp.snd(sp.fst(sp.snd(data.open_some())))
        # thumbnail_uri = sp.snd(sp.snd(data.open_some()))

        token_id = sp.compute(self.data.last_token_id)

        token_metadata = sp.record(
            token_id = token_id,
            token_info = sp.map(
                l = {
                    "name": name,
                    "description": description,
                    "artifact_uri": artifact_uri,
                    "display_uri": display_uri,
                    "thumbnail_uri": thumbnail_uri
                },
            )
        )
        
        # metadata = sp.record(token_id=token_id, token_info=action.metadata)
        self.data.token_metadata[token_id] = token_metadata
        self.data.ledger[token_id] = address
        self.data.last_token_id += 1

admin = sp.address('tz1iWU9xwe1gbboxefyWadcmFeg2yMMLQ8Ap')

token_metadata = FA2.make_metadata(
    name = "Sword Token",
    symbol = "SWRD",
    decimals = 0,
)

metadata_base = {
    "version": "1.0.0",
    "description" : "This implements FA2 (TZIP-012) using SmartPy.",
    "interfaces": ["TZIP-012", "TZIP-016"],
    "authors": ["SmartPy <https://smartpy.io/#contact>"],
    "homepage": "https://smartpy.io/ide?template=FA2.py",
    "source": {
        "tools": ["SmartPy"],
        "location": "https://gitlab.com/SmartPy/smartpy/-/raw/master/python/templates/FA2.py"
    },
    "permissions": {
        "receiver": "owner-no-hook",
        "sender": "owner-no-hook"
    }
}

sp.add_compilation_target(
    "Sword Token",
    Sword_Token(
        metadata = sp.utils.metadata_of_url("https://bafkreib4bkzjauwwueuve7dre7jd6noetopg2uenr7yu5qqju4ncdbu5je.ipfs.dweb.link/"),
        token_metadata = {},
        ledger = {},
        policy = None,
        metadata_base = None,
        admin = admin
    ),
)

@sp.add_test(name="Test_Sword_Token")
def test():
    scenario = sp.test_scenario()
    scenario.h1("Test Sword Token")
    scenario.h2("Deploy Sword Token")
    # scenario.h2(sp.utils.bytes_of_string("Hello world"))
    token = Sword_Token(
        admin = admin,
        metadata = sp.utils.metadata_of_url("https://bafkreib4bkzjauwwueuve7dre7jd6noetopg2uenr7yu5qqju4ncdbu5je.ipfs.dweb.link/"),
        token_metadata = {},
        ledger = {},
        policy = None,
        metadata_base = metadata_base
    )
    scenario.h2("Check Sword Token")
    scenario += token
    scenario.h2("Mint Sword Token")
    scenario += token.mint(
        sig = sp.signature("edsigtjFc1SCbcAAATa9V7NU2pNj6jbcatd1yy3R6SMmvSgfFdTenHQJoCf3QFnsgyAGtBCqR36BG82dGTUfw5fysjjY3kjs1bj"),
        data_bytes = sp.bytes("0x050707070707070a000000160000fadcd216de7817afb85f7f7a39510e2ed2243032000007070100000012353337373666373236343230346534363534010000002635343638363937333230363937333230363132303733373736663732363432303465343635340707070701000000b23638373437343730373333613266326636323631363636623732363536393635363536323632366537323334373836643730363436613335373536343333363537363737373337373632366537303730373133363733373633333734363436353663363237373335363337393663363436613636373137613337333636363735363233333739326536393730363637333265366536363734373337343666373236313637363532653663363936653662326601000000b23638373437343730373333613266326636323631363636623732363536393635363536323632366537323334373836643730363436613335373536343333363537363737373337373632366537303730373133363733373633333734363436353663363237373335363337393663363436613636373137613337333636363735363233333739326536393730363637333265366536363734373337343666373236313637363532653663363936653662326601000000b236383734373437303733336132663266363236313636366237323635363936353635363236323665373233343738366437303634366133353735363433333635373637373733373736323665373037303731333637333736333337343634363536633632373733353633373936633634366136363731376133373336363637353632333337393265363937303636373332653665363637343733373436663732363136373635326536633639366536623266"),
        data = sp.record(
            address = sp.address("tz1iWU9xwe1gbboxefyWadcmFeg2yMMLQ8Ap"),
            token_id = 0,
            name = sp.bytes("0x53776f7264204e4654"),
            description = sp.bytes("0x5468697320697320612073776f7264204e4654"),
            artifact_uri = sp.bytes("0x68747470733a2f2f6261666b726569656562626e7234786d70646a357564336576777377626e707071367376337464656c62773563796c646a66717a373666756233792e697066732e6e667473746f726167652e6c696e6b2f"),
            display_uri = sp.bytes("0x68747470733a2f2f6261666b726569656562626e7234786d70646a357564336576777377626e707071367376337464656c62773563796c646a66717a373666756233792e697066732e6e667473746f726167652e6c696e6b2f"),
            thumbnail_uri = sp.bytes("0x68747470733a2f2f6261666b726569656562626e7234786d70646a357564336576777377626e707071367376337464656c62773563796c646a66717a373666756233792e697066732e6e667473746f726167652e6c696e6b2f"),
        )
    )
    scenario += token.mint(
        sig = sp.signature("edsigtjFc1SCbcAAATa9V7NU2pNj6jbcatd1yy3R6SMmvSgfFdTenHQJoCf3QFnsgyAGtBCqR36BG82dGTUfw5fysjjY3kjs1bj"),
        data_bytes = sp.bytes("0x050707070707070a000000160000fadcd216de7817afb85f7f7a39510e2ed2243032000007070100000012353337373666373236343230346534363534010000002635343638363937333230363937333230363132303733373736663732363432303465343635340707070701000000b23638373437343730373333613266326636323631363636623732363536393635363536323632366537323334373836643730363436613335373536343333363537363737373337373632366537303730373133363733373633333734363436353663363237373335363337393663363436613636373137613337333636363735363233333739326536393730363637333265366536363734373337343666373236313637363532653663363936653662326601000000b23638373437343730373333613266326636323631363636623732363536393635363536323632366537323334373836643730363436613335373536343333363537363737373337373632366537303730373133363733373633333734363436353663363237373335363337393663363436613636373137613337333636363735363233333739326536393730363637333265366536363734373337343666373236313637363532653663363936653662326601000000b236383734373437303733336132663266363236313636366237323635363936353635363236323665373233343738366437303634366133353735363433333635373637373733373736323665373037303731333637333736333337343634363536633632373733353633373936633634366136363731376133373336363637353632333337393265363937303636373332653665363637343733373436663732363136373635326536633639366536623266")
    )
    