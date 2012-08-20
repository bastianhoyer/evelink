import mock
import unittest2 as unittest

import evelink.corp as evelink_corp
from tests.utils import APITestCase

class CorpTestCase(APITestCase):

    def setUp(self):
        super(CorpTestCase, self).setUp()
        self.corp = evelink_corp.Corp(api=self.api)

    @mock.patch('evelink.corp.parse_industry_jobs')
    def test_industry_jobs(self, mock_parse):
        self.api.get.return_value = mock.sentinel.industry_jobs_api_result
        mock_parse.return_value = mock.sentinel.industry_jobs

        result = self.corp.industry_jobs()

        self.assertEqual(result, mock.sentinel.industry_jobs)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/IndustryJobs'),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.industry_jobs_api_result),
            ])

    def test_npc_standings(self):
        self.api.get.return_value = self.make_api_result("corp/npc_standings.xml")

        result = self.corp.npc_standings()

        self.assertEqual(result, {
                'agents': {
                    3008416: {
                        'id': 3008416,
                        'name': 'Antaken Kamola',
                        'standing': 2.71,
                    },
                },
                'corps': {
                    1000003: {
                        'id': 1000003,
                        'name': 'Prompt Delivery',
                        'standing': 0.97,
                    },
                },
                'factions': {
                    500019: {
                        'id': 500019,
                        'name': "Sansha's Nation",
                        'standing': -4.07,
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Standings'),
            ])

    @mock.patch('evelink.corp.parse_kills')
    def test_kills(self, mock_parse):
        self.api.get.return_value = mock.sentinel.kills_api_result
        mock_parse.return_value = mock.sentinel.kills

        result = self.corp.kills()

        self.assertEqual(result, mock.sentinel.kills)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/KillLog', {}),
            ])
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.kills_api_result),
            ])

    @mock.patch('evelink.corp.parse_contracts')
    def test_contracts(self, mock_parse):
        self.api.get.return_value = mock.sentinel.contracts_api_result
        mock_parse.return_value = mock.sentinel.parsed_contracts

        result = self.corp.contracts()
        self.assertEqual(result, mock.sentinel.parsed_contracts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.contracts_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Contracts'),
            ])

    @mock.patch('evelink.corp.parse_contact_list')
    def test_contacts(self, mock_parse):
        self.api.get.return_value = mock.sentinel.contacts_api_result
        mock_parse.return_value = mock.sentinel.parsed_contacts

        result = self.corp.contacts()
        self.assertEqual(result, mock.sentinel.parsed_contacts)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.contacts_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/ContactList'),
            ])

    def test_wallet_info(self):
        self.api.get.return_value = self.make_api_result("corp/wallet_info.xml")

        result = self.corp.wallet_info()

        self.assertEqual(result, {
            1000: {'balance': 74171957.08, 'id': 4759, 'key': 1000},
            1001: {'balance': 6.05, 'id': 5687, 'key': 1001},
            1002: {'balance': 0.0, 'id': 5688, 'key': 1002},
            1003: {'balance': 17349111.0, 'id': 5689, 'key': 1003},
            1004: {'balance': 0.0, 'id': 5690, 'key': 1004},
            1005: {'balance': 0.0, 'id': 5691, 'key': 1005},
            1006: {'balance': 0.0, 'id': 5692, 'key': 1006},
        })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/AccountBalance'),
            ])

    @mock.patch('evelink.corp.parse_wallet_journal')
    def test_wallet_journal(self, mock_parse):
        self.api.get.return_value = mock.sentinel.journal_api_result
        mock_parse.return_value = mock.sentinel.parsed_journal

        result = self.corp.wallet_journal()
        self.assertEqual(result, mock.sentinel.parsed_journal)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.journal_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletJournal', {}),
            ])

    def test_wallet_journal_paged(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        self.corp.wallet_journal(before_id=1234)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletJournal', {'fromID': 1234}),
            ])

    def test_wallet_journal_limit(self):
        self.api.get.return_value = self.make_api_result("char/wallet_journal.xml")

        self.corp.wallet_journal(limit=100)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletJournal', {'rowCount': 100}),
            ])

    @mock.patch('evelink.corp.parse_wallet_transactions')
    def test_wallet_transcations(self, mock_parse):
        self.api.get.return_value = mock.sentinel.transactions_api_result
        mock_parse.return_value = mock.sentinel.parsed_transactions

        result = self.corp.wallet_transactions()
        self.assertEqual(result, mock.sentinel.parsed_transactions)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.transactions_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletTransactions', {}),
            ])

    def test_wallet_transactions_paged(self):
        self.api.get.return_value = self.make_api_result("char/wallet_transactions.xml")

        self.corp.wallet_transactions(before_id=1234)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletTransactions', {'fromID': 1234}),
            ])

    def test_wallet_transactions_limit(self):
        self.api.get.return_value = self.make_api_result("char/wallet_transactions.xml")

        self.corp.wallet_transactions(limit=100)
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/WalletTransactions', {'rowCount': 100}),
            ])

    @mock.patch('evelink.corp.parse_market_orders')
    def test_orders(self, mock_parse):
        self.api.get.return_value = mock.sentinel.orders_api_result
        mock_parse.return_value = mock.sentinel.parsed_orders

        result = self.corp.orders()
        self.assertEqual(result, mock.sentinel.parsed_orders)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.orders_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MarketOrders'),
            ])

    def test_faction_warfare_stats(self):
        self.api.get.return_value = self.make_api_result('corp/faction_warfare_stats.xml')

        result = self.corp.faction_warfare_stats()

        self.assertEqual(result, {
                'faction': {'id': 500001, 'name': 'Caldari State'},
                'kills': {'total': 0, 'week': 0, 'yesterday': 0},
                'pilots': 6,
                'points': {'total': 0, 'week': 1144, 'yesterday': 0},
                'start_ts': 1213135800,
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/FacWarStats'),
            ])

    @mock.patch('evelink.corp.parse_assets')
    def test_assets(self, mock_parse):
        self.api.get.return_value = mock.sentinel.assets_api_result
        mock_parse.return_value = mock.sentinel.parsed_assets

        result = self.corp.assets()
        self.assertEqual(result, mock.sentinel.parsed_assets)
        self.assertEqual(mock_parse.mock_calls, [
                mock.call(mock.sentinel.assets_api_result),
            ])
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/AssetList'),
            ])

    def test_shareholders(self):
        self.api.get.return_value = self.make_api_result("corp/shareholders.xml")

        result = self.corp.shareholders()

        self.assertEqual(result, {
                'char': {
                    126891489: {
                        'corp': {
                            'id': 632257314,
                            'name': 'Corax.',
                        },
                        'id': 126891489,
                        'name': 'Dragonaire',
                        'shares': 1,
                    },
                },
                'corp': {
                    126891482: {
                        'id': 126891482,
                        'name': 'DragonaireCorp',
                        'shares': 1,
                    },
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Shareholders'),
            ])

    def test_titles(self):
        self.api.get.return_value = self.make_api_result("corp/titles.xml")

        result = self.corp.titles()

        self.assertEqual(result, {
                1: {
                    'can_grant': {'at_base': {}, 'at_hq': {}, 'at_other': {}, 'global': {}},
                    'id': 1,
                    'name': 'Member',
                    'roles': {
                        'at_base': {},
                        'at_other': {},
                        'global': {},
                        'at_hq': {
                            8192: {
                                'description': 'Can take items from this divisions hangar',
                                'id': 8192,
                                'name': 'roleHangarCanTake1',
                            },
                        },
                    },
                },
                2: {
                    'can_grant': {'at_base': {}, 'at_hq': {}, 'at_other': {}, 'global': {}},
                    'id': 2,
                    'name': 'unused 1',
                    'roles': {'at_base': {}, 'at_hq': {}, 'at_other': {}, 'global': {}},
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/Titles'),
            ])

    def test_starbases(self):
        self.api.get.return_value = self.make_api_result("corp/starbases.xml")

        result = self.corp.starbases()

        self.assertEqual(result, {
                100449451: {
                    'id': 100449451,
                    'location_id': 30000163,
                    'moon_id': 40010395,
                    'online_ts': 1244098851,
                    'standings_owner_id': 673381830,
                    'state': 'online',
                    'state_ts': 1323374621,
                    'type_id': 27538,
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/StarbaseList'),
            ])

    def test_starbase_details(self):
        self.api.get.return_value = self.make_api_result("corp/starbase_details.xml")

        result = self.corp.starbase_details(123)

        self.assertEqual(result, {
                'combat': {
                    'hostility': {
                        'aggression': {'enabled': False},
                        'sec_status': {'enabled': False, 'threshold': 0.0},
                        'standing': {'enabled': True, 'threshold': 9.9},
                        'war': {'enabled': True},
                    },
                    'standings_owner_id': 154683985,
                },
                'fuel': {16274: 18758, 16275: 2447},
                'online_ts': 1240097429,
                'permissions': {
                    'deploy': {
                        'anchor': 'Starbase Config',
                        'offline': 'Starbase Config',
                        'online': 'Starbase Config',
                        'unanchor': 'Starbase Config',
                    },
                    'forcefield': {'alliance': True, 'corp': True},
                    'fuel': {
                        'take': 'Alliance Members',
                        'view': 'Starbase Config',
                    },
                },
                'state': 'online',
                'state_ts': 1241299896,
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/StarbaseDetail', {'itemID': 123}),
            ])

    def test_members(self):
        self.api.get.return_value = self.make_api_result("corp/members.xml")

        result = self.corp.members()

        self.assertEqual(result, {
                150336922: {
                    'base': {'id': 0, 'name': ''},
                    'can_grant': 0,
                    'id': 150336922,
                    'join_ts': 1181745540,
                    'location': {
                        'id': 60011566,
                        'name': 'Bourynes VII - Moon 2 - University of Caille School',
                    },
                    'logoff_ts': 1182029760,
                    'logon_ts': 1182028320,
                    'name': 'corpexport',
                    'roles': 0,
                    'ship_type': {'id': 606, 'name': 'Velator'},
                    'title': 'asdf',
                },
                150337897: {
                    'base': {'id': 0, 'name': ''},
                    'can_grant': 0,
                    'id': 150337897,
                    'join_ts': 1181826840,
                    'location': {
                        'id': 60011566,
                        'name': 'Bourynes VII - Moon 2 - University of Caille School',
                    },
                    'logoff_ts': 1182029700,
                    'logon_ts': 1182028440,
                    'name': 'corpslave',
                    'roles': 22517998271070336,
                    'ship_type': {'id': 670, 'name': 'Capsule'},
                    'title': '',
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/MemberTracking', {'extended': 1}),
            ])

    def test_stations(self):
        self.api.get.return_value = self.make_api_result("corp/stations.xml")

        result = self.corp.stations()

        self.assertEqual(result, {
                61000368: {
                    'docking_fee_per_volume': 0.0,
                    'id': 61000368,
                    'name': 'Station Name Goes Here',
                    'office_fee': 25000000,
                    'owner_id': 857174087,
                    'reprocessing': {'cut': 0.025, 'efficiency': 0.5},
                    'standing_owner_id': 673381830,
                    'system_id': 30004181,
                    'type_id': 21645,
                },
            })
        self.assertEqual(self.api.mock_calls, [
                mock.call.get('corp/OutpostList'),
            ])


if __name__ == "__main__":
    unittest.main()
